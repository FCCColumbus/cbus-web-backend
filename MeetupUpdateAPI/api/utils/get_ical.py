import requests
import logging
from . import parsing_ical
# might not need this: export_file_id = "15CscXC8lA0vGlAn9ZxjCX8628f0wStX24wK1DhbxBu4"




def get_techlife_calendar():
    
    # memberid = fcccolumbus614@gmail.com, file = tech_life_calendar.ics
    return export_meetup_calendar("276932425", "https://www.meetup.com/techlifecolumbus/events/ical/")
# ___________________________________________________________________________________________________________________________
def export_meetup_calendar(meetup_member_id, calendar_url):
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    try:
        cookie = f"MEETUP_MEMBER=id={meetup_member_id}&status=1&timestamp=1685662475&bs=0&tz=US%2FEastern&ql=false&scope=ALL&rem=1;"
        logger.info("Fetching events...")
        
        response = requests.get(calendar_url, headers={"cookie": cookie})
        response.raise_for_status()  # Raises an HTTPError for bad responses
     
        logger.info("Success!")
        return response.content 
    except Exception as e:
        logger.error(f"An exception occurred: {e}")
        raise

if __name__ == "__main__":
    get_techlife_calendar()