from django.db import models
from django.contrib.auth import get_user_model
from django_geopostcodes import GeoPostcodeField

User = get_user_model()

class MyModel(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=100)
    summary = models.TextField()
    description = models.TextField()
    event_class = models.CharField()
    author = models.ForeignKey(User, on_delete=models.CASCADE) #TODO: check the parameters if needed
    geo = GeoPostcodeField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    url = models.URLField()
    uuid = models.UUIDField()