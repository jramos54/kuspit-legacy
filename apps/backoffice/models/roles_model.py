
# Librerías de Terceros
from django.contrib.auth.models import Group
from django.contrib.gis.db import models


class RolesGroups(models.Model):
    group=models.ForeignKey(Group,on_delete=models.CASCADE)
    usedBy=models.CharField(max_length=255)

    class Meta:
        db_table="dyp_roles"

    def __str__(self):
        return f"{self.group.name} used by {self.usedBy}"
