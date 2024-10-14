import requests
import logging
import os
from dotenv import load_dotenv

load_dotenv()
# setup logger
logger = logging.getLogger(__name__)


def get_techlife_calendar():
    logger.info("Getting techlife calendar...")
    MEETUP_API_KEY = os.getenv('MEETUP_ID')
    MEETUP_EXPORT_URL = os.getenv('MEETUP_EXPORT_URL')
    return export_meetup_calendar(MEETUP_API_KEY, MEETUP_EXPORT_URL)
# ___________________________________________________________________________________________________________________________
def export_meetup_calendar(meetup_member_id, calendar_url):
    # Set up logging
    try:
        cookie = f"MEETUP_MEMBER=id={meetup_member_id}&status=1&timestamp=1685662475&bs=0&tz=US%2FEastern&ql=false&scope=ALL&rem=1;"
        logger.info("Fetching events...")
        
        response = requests.get(calendar_url, headers={"cookie": cookie})
        response.raise_for_status()  # Raises an HTTPError for bad responses
     
        logger.info("Success!")
        return response.content 
    except Exception as e:
        logger.error(f"An exception occurred while fetching data from meetup API: {e}")
        raise

if __name__ == "__main__":
    get_techlife_calendar()