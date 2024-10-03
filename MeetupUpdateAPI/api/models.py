from django.db import models
import pytz
from django.utils import timezone

# NOTE not parsing GEO attribute at the moment because it requires some more imports and logic. 
class MeetupIcalModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=100)
    summary = models.TextField()
    description = models.TextField()
    event_class = models.CharField(max_length=100)
    author = models.CharField(max_length=100) 
    location = models.CharField(max_length=255, blank=True)
    url = models.URLField()
    meetupUUID = models.CharField(max_length=200, default='')
    uuid = models.UUIDField()

    
    def __str__(self):
        return self.summary

        