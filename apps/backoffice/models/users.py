from compartidos.models import GeoTimestampedModel

# Librerías de Terceros
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, UserManager
from django.contrib.gis.db import models


class User(AbstractBaseUser, PermissionsMixin, GeoTimestampedModel):
    password = models.CharField(max_length=128)
    username = models.CharField(max_length=50, unique=True, null=True)
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    is_customer = models.BooleanField(default=False)
    is_persona_fisica = models.BooleanField(default=False)
    is_persona_moral = models.BooleanField(default=False)

    open_fin_id = models.IntegerField(null=True)
    payments_user_id = models.IntegerField(null=True)

    login_attempts = models.IntegerField(default=0, null=True)
    last_attempt = models.DateTimeField(null=True)

    location_date = models.DateTimeField(null=True)

    open_fin_token = models.TextField(null=True)
    open_fin_token_exp = models.IntegerField(null=True)
    open_fin_refresh = models.TextField(null=True)
    open_fin_refresh_exp = models.IntegerField(null=True)

    is_new_user = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def is_blocked(self):
        try:
            return self.login_attempts >= 3
        except TypeError:
            return False


class UserSecureCode(GeoTimestampedModel):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    code = models.IntegerField(null=True)
    expedition_datetime = models.DateTimeField(null=True)
    tries = models.IntegerField(default=0, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.code
