from django.test import TestCase
import os
from .utils.parsing_ical import parse_ical_file, map_model_parsed_file_to_class
from .models import MeetupIcalModel
from datetime import datetime
from io import BytesIO
import requests
import logging



class UtilsTests(TestCase):
    # base file path for tests
    @classmethod
    def setUpClass(cls):
        cls.FILE_PATH = "api/sample_tech_life_calendar.ics.txt"
    
    
# TESTS BEGIN****************************************************************************
# _______________________________________________________________________________________   
    # RESOURCE CHECK
# _______________________________________________________________________________________   


    def test_connection_to_meetup_api(self):
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

       
        # memberid = fcccolumbus614@gmail.com, file = tech_life_calendar.ics
        export_meetup_calendar("276932425", "https://www.meetup.com/techlifecolumbus/events/ical/", "15CscXC8lA0vGlAn9ZxjCX8628f0wStX24wK1DhbxBu4")

        def export_meetup_calendar(meetup_member_id, calendar_url, export_file_id):
            try:
                cookie = f"MEETUP_MEMBER=id={meetup_member_id}&status=1&timestamp=1685662475&bs=0&tz=US%2FEastern&ql=false&scope=ALL&rem=1;"
                logger.info("Fetching events...")
            
                response = requests.get(calendar_url, headers={"cookie": cookie})
                response.raise_for_status()  # Raises an HTTPError for bad responses
                logger.info("Success!")
            except Exception as e:
                logger.error(f"An exception occurred: {e}")
                raise

    def test_connection_to_ical_file(self):
        
        # Check if the file exists using os.path.exists()
        file_exists = os.path.exists(self.FILE_PATH)
        # Assert the expected result
        self.assertEqual(file_exists, True, f"File not found at path: {self.FILE_PATH}")
# _______________________________________________________________________________________   
    # PARSE CHECK  
    def test_output_of_parse_ical_file_func(self):
        parse_ical_output = parse_ical_file(self.FILE_PATH)
        uid_of_first_item = "event_vzhrctyfcmbsb@meetup.com"
        self.assertTrue(parse_ical_output[0]["UID"]==uid_of_first_item)
        
        
# _______________________________________________________________________________________   
    # DATABASE CHECKS
# _______________________________________________________________________________________   
    def test_if_data_saved_from_ical_file(self):
        # creating simple object for model
        model = MeetupIcalModel()
        model.created_at = datetime.now()
        model.start_time =  datetime.now()
        model.end_time = datetime.now()
        model.status = "Confirmed"
        model.summary = "Super cool event"
        model.description = "Lots of words"
        model.event_class = "Public"
        model.author = "FCCC"
        model.location = "Online"
        model.url = "www.google.com"
        model.meetupUUID = "1234"
        # saving to database
        model.save()
        # checking if saved
        if model.uuid:
            print(MeetupIcalModel.objects.get(pk=model.uuid))
            self.assertTrue("TEST: found database item")
        else: self.assertFalse("TEST: did not find in database")
        # checking if deleted
        MeetupIcalModel.objects.filter(pk=model.uuid).delete()
        self.assertFalse(MeetupIcalModel.objects.filter(pk=model.uuid),"TEST: Item was not deleted")

# _______________________________________________________________________________________   

    def test_if_bulk_save_works(self):
        # first model
        model = MeetupIcalModel()
        model.created_at = datetime.now()
        model.start_time =  datetime.now()
        model.end_time = datetime.now()
        model.status = "Confirmed"
        model.summary = "Super cool event"
        model.description = "Lots of words"
        model.event_class = "Public"
        model.author = "FCCC"
        model.location = "Online"
        model.url = "www.google.com"
        model.meetupUUID = "1234"
        # second model
        model2 = MeetupIcalModel()
        model2.created_at = datetime.now()
        model2.start_time =  datetime.now()
        model2.end_time = datetime.now()
        model2.status = "Confirmed"
        model2.summary = "Super cool event"
        model2.description = "Lots of words"
        model2.event_class = "Public"
        model2.author = "FCCC"
        model2.location = "Online"
        model2.url = "www.google.com"
        model2.meetupUUID = "1234"
        # adding models into array
        model_arr = [model,model2]
        # saving to database
        MeetupIcalModel.objects.bulk_create(model_arr)
        # checking if saved
        if model.uuid and model2:
            print(MeetupIcalModel.objects.get(pk=model.uuid))
            print(MeetupIcalModel.objects.get(pk=model2.uuid))
            self.assertTrue("TEST: found database item")
        else: self.assertFalse("TEST: did not find in database")
        # checking if deleted
        MeetupIcalModel.objects.filter(pk=model.uuid).delete()
        MeetupIcalModel.objects.filter(pk=model2.uuid).delete()
        self.assertFalse(MeetupIcalModel.objects.filter(pk=model.uuid),"TEST: Item was not deleted")
        self.assertFalse(MeetupIcalModel.objects.filter(pk=model2.uuid),"TEST: Item was not deleted")
# _______________________________________________________________________________________   
    # TEARDOWN
# _______________________________________________________________________________________   
    @classmethod
    def tearDownClass(cls):
        pass  # No cleanup needed for this test class