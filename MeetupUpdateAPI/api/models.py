from django.db import models
from django_geopostcodes import GeoPostcodeField


class MeetupIcalModel(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=100)
    summary = models.TextField()
    description = models.TextField()
    event_class = models.CharField()
    author = models.CharField(max_length=100) 
    geo = GeoPostcodeField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    url = models.URLField()
    uuid = models.UUIDField()

    
    def __str__(self):
        return self.summary

        