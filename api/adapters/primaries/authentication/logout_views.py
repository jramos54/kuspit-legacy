# Variables de Configuración
from configuracion.settings import URL_BASE_OPENFIN

from compartidos.serializers import NotFoundSerializer

# Librerías de Terceros
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone
from requests import request as external_request


class LogoutView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TokenRefreshSerializer

    @swagger_auto_schema(
        request_body=TokenRefreshSerializer,
        responses={
            status.HTTP_200_OK: TokenRefreshSerializer,
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            token = request.user.open_fin_token
            print(f"OpenFin Token {token}")

            if token is None:
                raise TokenError("No se ha enviado el token de autenticación")

            # logout from openfin
            url = f"http://{URL_BASE_OPENFIN}/rpc/logout"
            headers = {"Authorization": f"Bearer {token}"}
            response = external_request("POST", url, headers=headers)
            if response.status_code != 200:
                raise TokenError("Error al cerrar sesión en OpenFin")

            refresh_token = serializer.validated_data.get("refresh", None)

            if refresh_token:
                try:
                    token = RefreshToken(refresh_token)
                    token.blacklist()

                    current_time = timezone.now()
                    outstanding_tokens = OutstandingToken.objects.filter(
                        user=request.user, expires_at__gt=current_time
                    )

                    for outstanding_token in outstanding_tokens:
                        outstanding_token.expires_at = current_time
                        outstanding_token.save()

                except Exception as e:
                    print(f"Ocurrió una excepción inesperada: {e}")

            request.user.open_fin_token = None
            request.user.save()

        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(
            {"detail": "Has cerrado sesión correctamente"}, status=status.HTTP_200_OK
        )
