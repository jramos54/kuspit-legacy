# Librerías de Terceros
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.serializers import (
    update_last_login,
    TokenRefreshSerializer,
    PasswordField,
    RefreshToken,
)
from rest_framework_simplejwt.settings import api_settings
from typing import Any
from django.shortcuts import get_object_or_404

# para revisar si hay otra session abierta
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers, exceptions
from django.utils import timezone

# Proyecto
from .token_utils.token_functions import RefreshOpenfinToken
from ....engine.domain.exceptions import exceptions_users as exceptions
from ....engine.domain.messages import messages_users
from apps.backoffice.models import users as users_models


from ....adapters.secondaries.factory.constructor_email import constructor_user_dashboard as email_sender


emailSender = email_sender()


class OpenFinTokenRefreshSerializer(serializers.Serializer):
    """ "
    Esta clase se encarga de regresar el access token y refresh token
    """

    print("PASO 4 - clase OpenFinTokenRefreshSerializer")
    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)

    token_class = RefreshToken

    def validate(self, attrs):
        print("clase OpenFinTokenRefreshSerializer metodo validate")
        refresh = self.token_class(attrs["refresh"])

        data = {"access": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data["refresh"] = str(refresh)

        return data


class MyTokenObtainSerializer(serializers.Serializer):
    print("PASO 5 - clase MyTokenObtainSerializer")
    username_field = get_user_model().USERNAME_FIELD
    token_class = None

    default_error_messages = {
        "no_email_registered": _(exceptions.NoEmailregistered.msg),
        "invalid_password": _(exceptions.InvalidPassword.msg),
        "blocked_account": _(exceptions.BlockedAccount.msg),
        "many_sessions": _(exceptions.UserManySessions.msg),
        "user_inactive": _(exceptions.UserInactive.msg),
        "account_blocked": _(exceptions.AccountBlockedAdmin.msg),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields["password"] = PasswordField()
        self.user = None
        self.username=None
        self.user_email=None

    def validate(self, attrs):
        print("PASO 8 - clase MyTokenObtainSerializer metodo validate")
        # Preparar los argumentos para la autenticación
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        # Valida que el correo electronico este registrado
        try:
            user_check = get_user_model().objects.get(email=attrs[self.username_field])
        except get_user_model().DoesNotExist:
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_email_registered"],
                "no_email_registered",
            )

        # Verificar si el usuario está activo
        if not user_check.is_active:
            self.get_user_dashboard(attrs[self.username_field])
            messages = messages_users.AuthenticationMessages()
            message_send = messages.permanent_blocking_message(self.username, self.user_email)
            emailSender.send_email(self.user_email, message_send.get("asunto"), message_send.get("mensaje"), "token")
            raise exceptions.AuthenticationFailed(
                self.error_messages["user_inactive"],
                "user_inactive",
            )

        total_block_duration_minutes = 5
        # Verificar si la contraseña es correcta
        if not user_check.check_password(attrs["password"]):
            # Incrementar el contador de intentos fallidos si la contraseña es incorrecta
            user_check.login_attempts += 1
            user_check.last_attempt = timezone.now()
            user_check.save(update_fields=["login_attempts", "last_attempt"])

            if user_check.login_attempts > 3:
                self.get_user_dashboard(attrs[self.username_field])
                messages = messages_users.AuthenticationMessages()
                message_send = messages.temporal_blocking_message(self.username, self.user_email)
                emailSender.send_email(self.user_email, message_send.get("asunto"), message_send.get("mensaje"),
                                       "token")
                raise exceptions.AuthenticationFailed(
                    self.error_messages["account_blocked"],
                    "account_blocked",
                )

            else:
                # Lanzar excepción de contraseña incorrecta
                raise exceptions.AuthenticationFailed(
                    self.error_messages["invalid_password"],
                    "invalid_password",
                )

        elif user_check.is_blocked:
            # Cálculo del tiempo restante de bloqueo
            time_left = (
                total_block_duration_minutes
                - (timezone.now() - user_check.last_attempt).seconds / 60
            )
            try_in = f"{int(time_left)} minutos."
            print(try_in)
            if time_left <= 0:
                # Resetear los intentos de inicio de sesión y desbloquear la cuenta
                user_check.login_attempts = 0
                user_check.last_attempt = None
                user_check.save(update_fields=["login_attempts", "last_attempt"])
            else:
                # Lanzar excepción si la cuenta todavía está bloqueada
                raise (
                    exceptions.AuthenticationFailed(
                        self.error_messages["blocked_account"],
                        "blocked_account",
                    )
                )

        else:
            user_check.login_attempts = 0
            user_check.last_attempt = None
            user_check.save(update_fields=["login_attempts", "last_attempt"])

        # Autenticar al usuario
        self.user = authenticate(**authenticate_kwargs)

        if self.user:
            # Verifica si hay tokens no expirados para el usuario
            non_expired_tokens = OutstandingToken.objects.filter(
                user=self.user, expires_at__gt=timezone.now()
            )
            for token in non_expired_tokens:
                print(f"Token ID: {token.id}, Expira en: {token.expires_at}")

            # Si hay tokens no expirados, significa que hay otra sesión abierta
            if non_expired_tokens.exists():
                raise exceptions.AuthenticationFailed(
                    self.error_messages["many_sessions"],
                    "many_sessions",
                )

        if not self.user:
            raise exceptions.AuthenticationFailed(
                self.error_messages["invalid_credentials"],
                "invalid_credentials",
            )

        return {}

    @classmethod
    def get_token(cls, user, password):
        print("PASO 9 - clase MyTokenObtainSerializer metodo get_token")
        return cls.token_class.for_user(user, password)


    def get_user_dashboard(self,email) -> Any:
        """"""

        try:
            user = get_object_or_404(users_models.User, email=email)

            self.username=user.username
            self.user_email=user.email

        except Exception as error_exception:
            print(error_exception)
            return None

class TokenObtainPairSerializer(MyTokenObtainSerializer):
    print("PASO 6 - clase TokenObtainPairSerializer")
    token_class = RefreshOpenfinToken

    def validate(self, attrs):
        print("PASO 7 - clase TokenObtainPairSerializer metodo validate")
        data = super().validate(attrs)

        refresh, open_fin_token = self.get_token(self.user, attrs["password"])

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


def dyp_user_authentication_rule(user):
    # Prior to Django 1.10, inactive users could be authenticated with the
    # default `ModelBackend`.  As of Django 1.10, the `ModelBackend`
    # prevents inactive users from authenticating.  App designers can still
    # allow inactive users to authenticate by opting for the new
    # `AllowAllUsersModelBackend`.  However, we explicitly prevent inactive
    # users from authenticating to enforce a reasonable policy and provide
    # sensible backwards compatibility with older Django versions.
    print("metodo dyp_user_authentication_rule")
    if user.password == "":
        return False

    return user is not None


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)

    token_class = RefreshOpenfinToken

    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh"])

        data = {"access": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()
            data["refresh"] = str(refresh)

        return data
