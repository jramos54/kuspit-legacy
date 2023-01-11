from django.contrib.auth.models import Group
from django.contrib.gis.db import models
from .users import User


class Log2FA(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status_2fa = models.BooleanField(default=False)
    temp_code = models.CharField(max_length=6, null=True, blank=True)
    failed_attempts = models.IntegerField(default=0)
    questions_attempt = models.IntegerField(default=0)

    class Meta:
        db_table = "log_2fa"

    def __str__(self):
        return f"{self.user.name} status {self.status_2fa}"
