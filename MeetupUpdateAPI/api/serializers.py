from rest_framework import serializers
from .models import MeetupIcalModel
       
       
class MeetupIcalKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model: MeetupIcalModel
           
    fields = ['id', 'created_at', 'updated_at', 
          'start_time', 'end_time', 'status', 
          'summary', 'description', 'event_class', 
          'author_id', 'location', 
          'url', 'meetup_uuid']
