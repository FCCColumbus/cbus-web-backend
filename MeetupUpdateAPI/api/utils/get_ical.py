import requests
import logging
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def export_techlife_calendar():
    # memberid = fcccolumbus614@gmail.com, file = tech_life_calendar.ics
    export_meetup_calendar("276932425", "https://www.meetup.com/techlifecolumbus/events/ical/", "15CscXC8lA0vGlAn9ZxjCX8628f0wStX24wK1DhbxBu4")

def export_meetup_calendar(meetup_member_id, calendar_url, export_file_id):
    try:
        cookie = f"MEETUP_MEMBER=id={meetup_member_id}&status=1&timestamp=1685662475&bs=0&tz=US%2FEastern&ql=false&scope=ALL&rem=1;"
        logger.info("Fetching events...")
        
        response = requests.get(calendar_url, headers={"cookie": cookie})
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        write_ics_file(response.text, export_file_id)
        
        logger.info("Success!")
    except Exception as e:
        logger.error(f"An exception occurred: {e}")
        raise

def write_ics_file(content, export_file_id):
    try:
        # Setup the Drive v3 API
        creds = Credentials.from_authorized_user_file('path/to/your/credentials.json', ['https://www.googleapis.com/auth/drive.file'])
        service = build('drive', 'v3', credentials=creds)
        
        logger.info(f"file id is {export_file_id}...")
        
        # Get the file metadata
        file = service.files().get(fileId=export_file_id).execute()
        logger.info(f"Writing events to new {file['name']}...")
        
        # Create a BytesIO object from the content
        file_content = BytesIO(content.encode())
        
        # Create a media object
        media = MediaIoBaseUpload(file_content, mimetype='text/calendar', resumable=True)
        
        # Update the file content
        updated_file = service.files().update(
            fileId=export_file_id,
            media_body=media
        ).execute()
        
        logger.info(f"File updated successfully. File ID: {updated_file['id']}")
    except Exception as e:
        logger.error(f"An exception occurred: {e}")
        raise

if __name__ == "__main__":
    export_techlife_calendar()