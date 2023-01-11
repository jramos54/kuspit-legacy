# Librerias Estandar
import json

# Variables de Configuración
from configuracion.settings import URL_BASE_OPENFIN

# Librerías de Terceros
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken, Token
from rest_framework_simplejwt.utils import datetime_from_epoch
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.conf import settings
from requests import request


class OpenFinToken(Token):
    print("PASO 1 - clase OpenFinToken")

    @classmethod
    def for_user(cls, user, pswd):
        """
        Returns an authorization token for the given user that will be provided
        after authenticating the user's credentials.
        """
        print("PASO 11 - clase OpenFinToken metodo for_user")
        user_id = getattr(user, api_settings.USER_ID_FIELD)
        if not isinstance(user_id, int):
            user_id = str(user_id)

        token = cls()
        token[api_settings.USER_ID_CLAIM] = user_id

        return token


class BlacklistOpenfinMixin:
    """
    If the `rest_framework_simplejwt.token_blacklist` app was configured to be
    used, tokens created from `BlacklistMixin` subclasses will insert
    themselves into an outstanding token list and also check for their
    membership in a token blacklist.
    """

    print("PASO 2 - Clase BlacklistOpenfinMixin")
    if "rest_framework_simplejwt.token_blacklist" in settings.INSTALLED_APPS:

        def verify(self, *args, **kwargs):
            print(" Clase BlacklistOpenfinMixin metodo verify")
            self.check_blacklist()

            super().verify(*args, **kwargs)

        def check_blacklist(self):
            """
            Checks if this token is present in the token blacklist.  Raises
            `TokenError` if so.
            """
            print(" Clase BlacklistOpenfinMixin metodo check_blacklist")
            jti = self.payload[api_settings.JTI_CLAIM]

            if BlacklistedToken.objects.filter(token__jti=jti).exists():
                raise TokenError(_("Token is blacklisted"))

        def blacklist(self):
            """
            Ensures this token is included in the outstanding token list and
            adds it to the blacklist.
            """
            print(" Clase BlacklistOpenfinMixin metodo blacklist")
            jti = self.payload[api_settings.JTI_CLAIM]
            exp = self.payload["exp"]

            # Ensure outstanding token exists with given jti
            token, _ = OutstandingToken.objects.get_or_create(
                jti=jti,
                defaults={
                    "token": str(self),
                    "expires_at": datetime_from_epoch(exp),
                },
            )

            return BlacklistedToken.objects.get_or_create(token=token)

        @classmethod
        def for_user(cls, user, pswd):
            """
            Adds this token to the outstanding token list.
            """

            print("PASO 10 - Clase BlacklistOpenfinMixin metodo for user")
            print("Aqui se solicita el token de openfin")
            url = f"http://{URL_BASE_OPENFIN}/rpc/auth"
            user_email = user.email
            user_password = pswd
            payload = f"username={user_email}&pass={user_password}"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            response = request("POST", url, headers=headers, data=payload)
            response_data = json.loads(response.text)

            if response.status_code != 200:
                raise TokenError("Error al iniciar sesión en OpenFin")

            open_fin_token = response_data["token"]
            open_fin_token_exp = response_data["exp"]
            open_fin_refresh = response_data["refresh_token"]
            open_fin_refresh_exp = response_data["exp_refresh_token"]

            print(f"OpenFin Token:\n {open_fin_token}")
            print(f"OpenFin Refresh:\n {open_fin_refresh}")

            token = super().for_user(user, pswd)
            jti = token[api_settings.JTI_CLAIM]
            exp = token["exp"]

            OutstandingToken.objects.create(
                user=user,
                jti=jti,
                token=str(token),
                created_at=token.current_time,
                expires_at=datetime_from_epoch(exp),
            )
            user.open_fin_token = str(open_fin_token)
            user.open_fin_token_exp = open_fin_token_exp
            user.open_fin_refresh = str(open_fin_refresh)
            user.open_fin_refresh_exp = open_fin_refresh_exp

            user.save()

            return token, open_fin_token

        @classmethod
        def refresh_external_token(cls, user, refresh_token):
            print("Clase BlacklistOpenfinMixin metodo refresh_external_token")
            url = f"http://{URL_BASE_OPENFIN}/rpc/refresh_token"
            token = f"Bearer {user.open_fin_token}"
            refresh = f"{user.open_fin_refresh}"
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "refresh": refresh,
                "Authorization": token,
            }
            response = request("POST", url, headers=headers)
            response_data = json.loads(response.text)

            if response.status_code != 200:
                raise TokenError("Error al refrescar el token en OpenFin")

            open_fin_token = response_data["token"]
            print(response_data)
            print(f"Refreshed OpenFin Token:\n {open_fin_token}")
            user.open_fin_token = str(open_fin_token)
            user.save()

            return open_fin_token


class RefreshOpenfinToken(BlacklistOpenfinMixin, OpenFinToken):
    print("PASO 3 - Clase RefreshOpenfinToken")
    token_type = "refresh"
    lifetime = api_settings.REFRESH_TOKEN_LIFETIME
    no_copy_claims = (
        api_settings.TOKEN_TYPE_CLAIM,
        "exp",
        # Both of these claims are included even though they may be the same.
        # It seems possible that a third party token might have a custom or
        # namespaced JTI claim as well as a default "jti" claim.  In that case,
        # we wouldn't want to copy either one.
        api_settings.JTI_CLAIM,
        "jti",
    )
    access_token_class = AccessToken

    @property
    def access_token(self):
        """
        Returns an access token created from this refresh token.  Copies all
        claims present in this refresh token to the new access token except
        those claims listed in the `no_copy_claims` attribute.
        """
        print("PASO 12 - Clase RefreshOpenfinToken metodo access_token")

        # Use instantiation time of refresh token as relative timestamp for
        # access token "exp" claim.  This ensures that both a refresh and
        # access token expire relative to the same time if they are created as
        # a pair.
        access = self.access_token_class()
        access.set_exp(from_time=self.current_time)

        no_copy = self.no_copy_claims
        for claim, value in self.payload.items():
            if claim in no_copy:
                continue
            access[claim] = value

        user_id = self.payload.get(api_settings.USER_ID_CLAIM)
        user = get_user_model().objects.get(pk=user_id)
        refresh_token = str(self)
        open_fin_token = self.refresh_external_token(user, refresh_token)
        access["open_fin_token"] = open_fin_token

        return access
