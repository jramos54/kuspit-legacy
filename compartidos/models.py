from django.contrib.gis.db import models


class TimestampedModel(models.Model):
    """
    Base model to add creation and update
    timestamp to models
    """

    created_at = models.DateTimeField(
        auto_now_add=True, editable=False
    )
    updated_at = models.DateTimeField(
        auto_now=True, editable=False
    )

    class Meta:
        abstract = True


class GeoTimestampedModel(TimestampedModel):
    """
    Base model to add creation and update
    geotimestamp to models
    """

    location = models.PointField(null=True, blank=True)

    class Meta:
        abstract = True


