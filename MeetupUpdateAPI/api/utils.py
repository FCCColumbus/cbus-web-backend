from datetime import datetime
from icalendar import Calendar, Event
from .models import MeetupIcalModel
import re




# Parse ical TODO: currently set to parse txt file. Replace with icalendar logic after testing.
# TODO: need to add error handling for all functions.
# *********************************************************************************************
# MAIN FUNCTIONS
# _____________________________________________________________________________________________
# PARSING 


def parse_ical_file(file_path) -> list:
    """Extracts events between "BEGIN:VEVENT" and "END:VEVENT" from a text file using Regex.

    Args:
        file_path (str): The path to the text file.

    Returns:
        list: A list of dictionaries, each representing an event from Meetup.com with its start times, end times, and other attributes.
    """

    events = []
    with open(file_path, 'r') as f:
        text = f.read()

        # Regular expression to match events
        pattern = r"BEGIN:VEVENT\n(.*?)\nEND:VEVENT"

        for match in re.findall(pattern, text, re.DOTALL):
            # create a dictionary with match
            my_dict = {}
            # split str based on n/
            lines = match.splitlines() 
            try: 
                # iterate and assign
                for line in lines:
                    if ':' in line:
                    # split str based on first colon
                        key, value = line.split(":",1)
                    # first part is set to key and last part to value
                        my_dict[key] = value
                    else: pass
                    # passing weird strings with multiple colons for now
            except ValueError:
                # TODO: handle value error for parser
                 pass
            # append obj to events
            events.append(my_dict)
    return events
# _____________________________________________________________________________________________
# MAPPING

def map_model_parsed_file_to_class(parsed_list) -> list:
    """Maps parsed datasource to object model

    Args:
        parsed_list (list): this is a list of dictionaries that have been parsed

    Returns:
        list: this returns a list of MeetupIcalModel objects
    """
    mappedEvents = []
    for event in parsed_list:
        model = MeetupIcalModel()
        model.created_at = event.get('DTSTAMP')
        model.start_time = event.get('DTSTART;TZID=America/New_York')
        model.end_time = event.get('DTEND;TZID=America/New_York')
        model.status = event.get('STATUS')
        model.summary = event.get('SUMMARY')
        model.description = event.get('DESCRIPTION')
        model.event_class = event.get('CLASS')
        model.author = event.get('CREATED')
        model.location = event.get('LOCATION', "") 
        model.url = event.get('URL')
        model.meetupUUID = event.get('UID')
        mappedEvents.append(model)
    return mappedEvents
# _____________________________________________________________________________________________
# DATABASE CRUD OPERATIONS

def delete_single_object(Model, model_uuid):
    """deletes an item from the database

    Args:
        Model (database_model): any model in the Models.py
        model_uuid (model_uuid): the model object's database uuid that it is assigned
    """
    Model.objects.filter(pk=model_uuid).delete()
    if not Model.objects.get(uuid=model_uuid):
        print("Item deleted")
        
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

# _____________________________________________________________________________________________
# *********************************************************************************************
# LOGIC
# _____________________________________________________________________________________________


# Current file is local. Eventually call it from Meetup api. 
icalFile = '/home/guregu/Gitter/FCCC_basic_DJANGO_API/MeetupUpdateAPI/api/sample_tech_life_calendar.ics.txt'

# returning list of event objects that match the database model after parsing and mapping
mappedEvents = map_model_parsed_file_to_class(parse_ical_file(icalFile))

# Save to database
print("Saving to database")
MeetupIcalModel.objects.bulk_create(mappedEvents)

# Check if the data has been saved
count_after = MeetupIcalModel.objects.count()
print(f"Number of objects in the database: {count_after}")

if count_after > 0:
    print("Data saved successfully!")
else:
    print("No data was saved.")



# ICALENDAR LOGIC
#  with open(file_path, 'rb') as file:
#         cal = Calendar.from_ical(file.read())
#         print(cal)

#     for event in cal.walk('VEVENT'):
#         start_time = event.get('dtstart').dt
#         end_time = event.get('dtend').dt
#         print(f"Event: {event.get('summary')}")
#         print(f"Start time: {start_time}")
#         print(f"End time: {end_time}")
#         if isinstance(start_time, datetime):
#             start_time = start_time.astimezone(pytz.timezone('America/New_York'))
#         if isinstance(end_time, datetime):
#             end_time = end_time.astimezone(pytz.timezone('America/New_York'))

#         obj, created = MeetupIcalModel.objects.update_or_create(
#             uuid=event.get('uid'),
#             defaults={
#                 'created_at': datetime.now(),
#                 'updated_at': datetime.now(),
#                 'start_time': start_time,
#                 'end_time': end_time,
#                 'status': event.get('status', ''),
#                 'summary': event.get('summary', ''),
#                 'description': event.get('description', ''),
#                 'event_class': event.get('class', ''),
#                 'author': 'Meetup',
#                 'location': event.get('location', ''),
#                 'url': event.get('url', ''),
#             }
#         )
#         if created:
#             print(f"Created new MeetupIcalModel instance: {obj.uuid}")
#         else:
#             print(f"Updated existing MeetupIcalModel instance: {obj.uuid}")