from datetime import datetime
import icalendar
from ..models import MeetupIcalModel
import re
from .get_ical import export_techlife_calendar
import pytz




# Parse ical TODO: currently set to parse txt file. Replace with icalendar logic after testing.
# TODO: need to add error handling for all functions.
# *********************************************************************************************
# MAIN FUNCTIONS
# *********************************************************************************************
# _____________________________________________________________________________________________
# GET DATA FROM MEETUP 

# _____________________________________________________________________________________________
# PARSING 

def parse_ical_file_with_icalendar(response_data: bytes) -> list:
    """Extracts events between "BEGIN:VEVENT" and "END:VEVENT" from a json request in bytes using icalendar import

    Args:
        response_data (bytes): The response data from the server containing the iCalendar data.

    Returns:
        list: A list of dictionaries, each representing an event from Meetup.com with its start times, end times, and other attributes.
    """
    try:
        # Decode the response data (bytes) into a string
        response_text = response_data.decode('utf-8')
        
        # Parse the iCalendar data
        calendar = icalendar.Calendar.from_ical(response_text)
        
        events = []
        for event in calendar.walk('VEVENT'):
            start_time = event.get('dtstart').dt
            end_time = event.get('dtend').dt
            
            # Convert to America/New_York timezone if datetime
            if isinstance(start_time, datetime):
                start_time = start_time.astimezone(pytz.timezone('America/New_York'))
            if isinstance(end_time, datetime):
                end_time = end_time.astimezone(pytz.timezone('America/New_York'))
            
            event_data = {
                'uuid': event.get('uid'),
                'start_time': start_time,
                'end_time': end_time,
                'status': event.get('status', ''),
                'summary': event.get('summary', ''),
                'description': event.get('description', ''),
                'event_class': event.get('class', ''),
                'location': event.get('location', ''),
                'url': event.get('url', ''),
            }
            events.append(event_data)
        print("list of events: " , events[0]["summary"])
        return events

    except Exception as e:
        print(f"An error occurred while parsing the iCalendar data: {e}")
        return []
# ____________________________________________________________________________________________________________________ 
def parse_ical_file_with_regex(file_string_data: str) -> list:
    """Extracts events between "BEGIN:VEVENT" and "END:VEVENT" from a text file using Regex.

    Args:
        file_path (str): The path to the text file.

    Returns:
        list: A list of dictionaries, each representing an event from Meetup.com with its start times, end times, and other attributes.
    """

    events = []

    text = file_string_data
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
        model.start_time = event.get('start_time')
        model.end_time = event.get('end_time')
        model.status = event.get('status')
        model.summary = event.get('summary')
        model.description = event.get('description')
        model.event_class = event.get('event_class')
        model.location = event.get('location', "") 
        model.url = event.get('url')
        model.meetupUUID = event.get('uuid')
        mappedEvents.append(model)
    return mappedEvents


# _____________________________________________________________________________________________
# *********************************************************************************************
# LOGIC
# _____________________________________________________________________________________________


# Current file is local. Eventually call it from Meetup api. 
# icalFile = '/home/guregu/Gitter/FCCC_basic_DJANGO_API/MeetupUpdateAPI/api/sample_tech_life_calendar.ics.txt'
icalFile = export_techlife_calendar()

# returning list of event objects that match the database model after parsing and mapping
mappedEvents = map_model_parsed_file_to_class(parse_ical_file_with_icalendar(icalFile))

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


# END OF CODE
# **************************************************************************************** 
# **************************************************************************************** 



