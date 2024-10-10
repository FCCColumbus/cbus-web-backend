from django.db import models
import pytz
from django.utils import timezone
import uuid

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
    # author = models.CharField(max_length=100) 
    location = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField()
    meetupUUID = models.CharField(max_length=200, default='')
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def save(self, *args, **kwargs):
        if self.start_time and timezone.is_naive(self.start_time):
            self.start_time = timezone.make_aware(self.start_time)
        if self.end_time and timezone.is_naive(self.end_time):
            self.end_time = timezone.make_aware(self.end_time)
        super().save(*args, **kwargs)
    
    
    def __str__(self):
        return self.summary

        