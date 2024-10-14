from ..models import MeetupIcalModel
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist


def delete_single_object(Model, model_uuid):
    """deletes an item from the database

    Args:
        Model (database_model): any model in the Models.py
        model_uuid (model_uuid): the model object's database uuid that it is assigned
    """
    Model.objects.filter(pk=model_uuid).delete()
    if not Model.objects.get(uuid=model_uuid):
        print("Item deleted")
        
# ___________________________________________________________________________________________________________________________

def delete_from_list_of_objects(Model, arr):
    """deletes items in the database from a list of objects

    Args:
        Model (database_model): any model in the Models.py
        model_uuid (list): the list of objects to delete
    """
    for item in arr:
        Model.objects.filter(pk=item.uuid).delete()
        if Model.objects.filter(pk=item.uuid):
                print(f"{item} event was not deleted")

# ___________________________________________________________________________________________________________________________

def get_single_object(Model, model_uuid):
    """gets an item from the database

    Args:
        Model (database_model): any model in the Models.py
        model_uuid (model_uuid): the model object's database uuid that it is assigned
    """
    if Model.objects.get(pk=model_uuid):
        return Model.objects.get(pk=model_uuid)

    if not Model.objects.get(pk=model_uuid):
        return "Item not found"
# ___________________________________________________________________________________________________________________________


def get_objects_by_attribute(Model, attribute: str, value: str):# -> QuerySet | None:
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
        return Model.objects.filter(**{attribute: value})
    except ObjectDoesNotExist:
        return Model.objects.none()


# ___________________________________________________________________________________________________________________________
        
def update_and_save_events_to_database(mappedEvents:list):
    """Takes the events that are mapped to the model, checks if they exist in the database, 
    and either creates new ones or updates existing ones. It then saves them to the database.

    Args:
        mappedEvents (list): list of MeetupIcalModel objects (dictionaries)

    Returns:
        None/Void
    """
    new_events = []
    existing_events = []
    existing_uuids = set(MeetupIcalModel.objects.values_list('meetupUUID', flat=True))

    for event in mappedEvents:
        if event.meetupUUID not in existing_uuids:
            new_events.append(event)
        else:
            existing_events.append(event)

    with transaction.atomic():
        # Save new events to database
        print("Saving new events to database")
        MeetupIcalModel.objects.bulk_create(new_events)

        # Update existing events
        if existing_events:
            print("Updating existing events")
            fields_to_update = [f.name for f in MeetupIcalModel._meta.fields 
                                if f.name not in ['meetupUUID', 'id']]
            MeetupIcalModel.objects.bulk_update(existing_events, fields_to_update)

    count_after = MeetupIcalModel.objects.count()
    print(f"Number of objects in the database: {count_after}")
    print(f"New events created: {len(new_events)}")
    print(f"Existing events updated: {len(existing_events)}")

    if count_after > 0:
        print("Data saved successfully!")
    else:
        print("No data was saved.")

# You can call this function when needed, not at module import time