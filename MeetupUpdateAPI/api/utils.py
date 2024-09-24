from datetime import datetime
import pytz
from icalendar import Calendar, Event
from .models import MeetupIcalModel



# Parse ical
def parse_ical_file(file_path):
    with open(file_path, 'rb') as file:
        cal = Calendar.from_ical(file.read())

    for event in cal.walk('VEVENT'):
        start_time = event.get('dtstart').dt
        end_time = event.get('dtend').dt
        if isinstance(start_time, datetime):
            start_time = start_time.astimezone(pytz.timezone('America/New_York'))
        if isinstance(end_time, datetime):
            end_time = end_time.astimezone(pytz.timezone('America/New_York'))

        obj, created = MeetupIcalModel.objects.update_or_create(
            uuid=event.get('uid'),
            defaults={
                'created_at': datetime.now(),
                'updated_at': datetime.now(),
                'start_time': start_time,
                'end_time': end_time,
                'status': event.get('status', ''),
                'summary': event.get('summary', ''),
                'description': event.get('description', ''),
                'event_class': event.get('class', ''),
                'author': 'Meetup',
                'location': event.get('location', ''),
                'url': event.get('url', ''),
            }
        )
        if created:
            print(f"Created new MeetupIcalModel instance: {obj.uuid}")
        else:
            print(f"Updated existing MeetupIcalModel instance: {obj.uuid}")

            
parse_ical_file('./sample_tech_life_calendar.ics.txt')