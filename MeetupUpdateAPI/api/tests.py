from django.test import TestCase
import os
from .utils.parsing_ical import parse_ical_file_with_icalendar, map_model_parsed_file_to_class, parse_ical_file_with_regex, update_meetup_events
from .models import MeetupIcalModel
from datetime import datetime
from io import BytesIO
import logging
from .utils.get_ical import export_meetup_calendar, export_techlife_calendar
from django.conf import settings



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
        # memberid = fcccolumbus614@gmail.com, file = tech_life_calendar.ics
        if export_meetup_calendar("276932425", "https://www.meetup.com/techlifecolumbus/events/ical/"):
            self.assertTrue("TEST: Connection to Meetup API was successful")


# _______________________________________________________________________________________   
    # PARSE CHECK  
    def test_output_of_parse_ical_file_func(self):
        json_from_meetup = export_techlife_calendar()
        # Decode the response data (bytes) into a string
        self.assertTrue(len(json_from_meetup)>0, "no data pulled")
        self.assertTrue(type(json_from_meetup)==bytes,"incorrect datatype")
        self.assertTrue(type(parse_ical_file_with_icalendar(json_from_meetup)==list), "incorrect datatype. Must be a list")
        calendar_item = parse_ical_file_with_icalendar(json_from_meetup)[0]
        self.assertTrue(type(calendar_item)==dict, "incorrect datatype. Must be a dict")
        
# _______________________________________________________________________________________   
    # SECURITY CHECKS
    def test_secret_key(self):
        # Check if the SECRET_KEY environment variable is set
        secret_key = os.environ.get('SECRET_KEY')
        api_key = settings.SECRET_KEY
        self.assertIsNotNone(secret_key, "TEST: SECRET_KEY environment variable is not set")
        self.assertTrue(secret_key == api_key, "TEST: SECRET_KEY environment variable does not match settings.SECRET_KEY")
# _______________________________________________________________________________________    
        
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
        # model.author = "FCCC"
        model.location = "Online"
        model.url = "www.google.com"
        model.meetupUUID = "1234"
        # saving to database
        model.save()
        # checking if saved
        if model.uuid:
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
        # model.author = "FCCC"
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
        # model2.author = "FCCC"
        model2.location = "Online"
        model2.url = "www.google.com"
        model2.meetupUUID = "1234"
        # adding models into array
        model_arr = [model,model2]
        # saving to database
        MeetupIcalModel.objects.bulk_create(model_arr)
        # checking if saved
        if model.uuid and model2:
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