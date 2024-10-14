from ..models import MeetupIcalModel
from .get_ical import get_techlife_calendar
from .parsing_ical import parse_icalendar_and_map_events
from django.core.exceptions import ObjectDoesNotExist
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
import logging
from django.db import transaction, DatabaseError, IntegrityError, OperationalError
from django.db.utils import DataError

# setup logger
logger = logging.getLogger(__name__)

# TODO: add error handling

def delete_single_object(Model, model_uuid):
    """
    Deletes an item from the database

    Args:
        Model (database_model): any model in the Models.py
        model_uuid (model_uuid): the model object's database uuid that it is assigned

    Returns:
        bool: True if deletion was successful, False if object not found

    Raises:
        DatabaseError: If there's an issue with the database operation
    """
    try:
        obj = Model.objects.get(uuid=model_uuid)
        obj.delete()
        logger.info(f"Successfully deleted {Model.__name__} object with UUID: {model_uuid}")
        return True

    except ObjectDoesNotExist:
        logger.warning(f"{Model.__name__} object with UUID: {model_uuid} not found")
        return False

    except DatabaseError as e:
        logger.error(f"Database error occurred while deleting {Model.__name__} object with UUID: {model_uuid}. Error: {str(e)}")
        raise

    except Exception as e:
        logger.error(f"Unexpected error occurred while deleting {Model.__name__} object with UUID: {model_uuid}. Error: {str(e)}")
        raise
        
# ___________________________________________________________________________________________________________________________

def delete_from_list_of_objects(Model, arr):
    """Deletes items in the database from a list of objects

    Args:
        Model (database_model): any model in the Models.py
        arr (list): the list of objects to delete
    """
    for item in arr:
        try:
            Model.objects.filter(pk=item.uuid).delete()
            if Model.objects.filter(pk=item.uuid).exists():
                logger.warning(f"{item} event was not deleted")
            else:
                logger.info(f"{item} event was successfully deleted")
        except ObjectDoesNotExist:
            logger.warning(f"{Model.__name__} object with UUID: {item.model_uuid} not found")
            return False 
        except Exception as e:
            logger.error(f"Error deleting {item}: {str(e)}")

# ___________________________________________________________________________________________________________________________

def get_single_object(Model, model_uuid):
    """Gets an item from the database

    Args:
        Model (database_model): any model in the Models.py
        model_uuid (model_uuid): the model object's database uuid that it is assigned

    Returns:
        Model instance or None: The requested object or None if not found
    """
    try:
        obj = Model.objects.get(pk=model_uuid)
        logger.info(f"Retrieved object with UUID: {model_uuid}")
        return obj
    except ObjectDoesNotExist as e:
        logger.error(f"Error retrieving object with UUID {model_uuid}: {str(e)}")
        return None
# ___________________________________________________________________________________________________________________________

def get_objects_by_attribute(Model, attribute: str, value: str):
    """
    Gets items from the database based on an attribute value.

    Args:
        Model: Any model class from Models.py
        attribute (str): The name of the attribute to filter by
        value (str): The value to match

    Returns:
        QuerySet: A queryset of matching objects, which may be empty if no objects are found
    """
    try:
        queryset = Model.objects.filter(**{attribute: value})
        logger.info(f"Retrieved {queryset.count()} objects with {attribute}={value}")
        return queryset
    except ObjectDoesNotExist as e:
        logger.error(f"Error retrieving object(s) with attribute: {attribute}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error retrieving objects with {attribute}={value}: {str(e)}")
        return Model.objects.none()
# ___________________________________________________________________________________________________________________________



def update_and_save_events_to_database(mappedEvents: list):
    """Takes the events that are mapped to the model, checks if they exist in the database, 
    and either creates new ones or updates existing ones. It then saves them to the database.

    Args:
        mappedEvents (list): list of MeetupIcalModel objects (dictionaries)

    Returns:
        tuple: (bool success, str message)
    """
    try:
        new_events = []
        existing_events = []
        
        try:
            existing_uuids = set(MeetupIcalModel.objects.values_list('meetupUUID', flat=True))
        except OperationalError as e:
            logger.error(f"Database operational error when fetching existing UUIDs: {str(e)}")
            return False, "Database operational error"
        except DatabaseError as e:
            logger.error(f"Database error when fetching existing UUIDs: {str(e)}")
            return False, "Database error"

        for event in mappedEvents:
            if event.meetupUUID not in existing_uuids:
                new_events.append(event)
            else:
                existing_events.append(event)

        try:
            with transaction.atomic():
                logger.info("Saving new events to database")
                MeetupIcalModel.objects.bulk_create(new_events)

                if existing_events:
                    logger.info("Updating existing events")
                    fields_to_update = [f.name for f in MeetupIcalModel._meta.fields 
                                        if f.name not in ['meetupUUID', 'id']]
                    MeetupIcalModel.objects.bulk_update(existing_events, fields_to_update)

        except IntegrityError as e:
            logger.error(f"Integrity error during bulk create/update: {str(e)}")
            return False, "Data integrity error"
        except DataError as e:
            logger.error(f"Data error during bulk create/update: {str(e)}")
            return False, "Invalid data error"
        except DatabaseError as e:
            logger.error(f"Database error during bulk create/update: {str(e)}")
            return False, "Database error"

        try:
            count_after = MeetupIcalModel.objects.count()
            logger.info(f"Number of objects in the database: {count_after}")
            logger.info(f"New events created: {len(new_events)}")
            logger.info(f"Existing events updated: {len(existing_events)}")

            if count_after > 0:
                logger.info("Data saved successfully!")
                return True, "Data saved successfully"
            else:
                logger.warning("No data was saved.")
                return False, "No data was saved"

        except DatabaseError as e:
            logger.error(f"Database error when counting objects: {str(e)}")
            return False, "Error verifying data save"

    except Exception as e:
        logger.error(f"Unexpected error updating and saving events: {str(e)}")
        return False, "Unexpected error occurred"

# ___________________________________________________________________________________________________________________________

def rate_limited_auto_update():
    """
    This function wraps the auto_update function and ensures it's not called
    more than once per hour.
    """
    CACHE_KEY = 'last_auto_update_time'
    now = timezone.now()
    last_execution = cache.get(CACHE_KEY)
    
    if last_execution is None or now - last_execution > timedelta(hours=1):
        try:
            # export data from api
            ical_events = get_techlife_calendar()
            logger.info("Parsing iCal data")
            # parse data and map to model
            mapped_events = parse_icalendar_and_map_events(ical_events)
            # process into database
            update_and_save_events_to_database(mapped_events)
            # update cache with current time
            cache.set(CACHE_KEY, now, timeout=3600)  # Set cache to expire in 1 hour
            logger.info(f"Auto-update performed successfully. Last update: {CACHE_KEY}")
        except Exception as e:
            logger.error(f"Error during auto_update: {str(e)}")
    else:
        time_since_last = now - last_execution
        logger.info(f"Update skipped. Last update was {time_since_last.total_seconds() / 60:.2f} minutes ago")
