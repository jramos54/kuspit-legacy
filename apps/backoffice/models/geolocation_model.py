from django.contrib.gis.db import models
from django.conf import settings


class Geolocation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.PointField(geography=True)
    service = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'geolocation_table'
