from datetime import datetime
import pytz
from icalendar import Calendar, Event
from .models import MeetupIcalModel
import re



# Parse ical TODO: currently set to parse txt file. Replace with icalendar logic after testing.
def parse_ical_file(file_path) -> list:
    """Extracts events between "BEGIN:VEVENT" and "END:VEVENT" from a text file.

    Args:
        file_path (str): The path to the text file.

    Returns:
        list: A list of dictionaries, each representing an event with its start and end times.
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
                    # split str based on colon
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


# Current file is local. Eventually call it from Meetup api. 
parse_ical_file('/home/guregu/Gitter/FCCC_basic_DJANGO_API/MeetupUpdateAPI/api/sample_tech_life_calendar.ics.txt')



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