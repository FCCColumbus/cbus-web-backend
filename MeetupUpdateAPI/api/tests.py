from django.test import TestCase
import os
from .utils import parse_ical_file



class UtilsTests(TestCase):
    # base file path for tests
    @classmethod
    def setUpClass(cls):
        cls.FILE_PATH = "api/sample_tech_life_calendar.ics.txt"
    
    
# _______________________________________________________________________________________   
    # TESTS BEGIN
# _______________________________________________________________________________________   
    def test_connection_to_ical_file(self):
        
        # Check if the file exists using os.path.exists()
        file_exists = os.path.exists(self.FILE_PATH)
        # Assert the expected result
        self.assertEqual(file_exists, True, f"File not found at path: {self.FILE_PATH}")
# _______________________________________________________________________________________   

    def test_output_of_parse_ical_file_func(self):
        parse_ical_output = parse_ical_file(self.FILE_PATH)
        uid_of_first_item = "event_vzhrctyfcmbsb@meetup.com"
        self.assertTrue(parse_ical_output[0]["UID"]==uid_of_first_item)
        
        
# _______________________________________________________________________________________   
    @classmethod
    def tearDownClass(cls):
        pass  # No cleanup needed for this test class