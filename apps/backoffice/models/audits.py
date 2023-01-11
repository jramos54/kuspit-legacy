from compartidos.models import GeoTimestampedModel

# Librerías de Terceros
from django.contrib.gis.db import models


class AuditModel(GeoTimestampedModel):
    """
    Base model to add creation and update
    timestamp to models
    """

    request_method = models.CharField(max_length=15)

    created_by = models.ForeignKey(
        "backoffice.User", on_delete=models.SET_NULL, null=True, blank=True
    )

    table_modified = models.CharField(max_length=50, null=True, blank=True)
    columns_modified = models.CharField(max_length=50, null=True, blank=True)
    row_modified = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.table_modified} table_modified by {self.created_by} using {self.request_method} method"
