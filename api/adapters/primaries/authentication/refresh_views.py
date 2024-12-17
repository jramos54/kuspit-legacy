# Librerías de Terceros
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

# Proyecto
from .token_utils.token_functions import RefreshOpenfinToken
from .swagger_docs import token_refresh_docs


class CustomTokenRefreshView(TokenRefreshView):
    @token_refresh_docs
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            # raise InvalidToken(e.args[0])
            return Response({"detail": e.args[0]}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshOpenfinToken(serializer.validated_data["refresh"])
        data = {"access": str(refresh.access_token)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()
            data["refresh"] = str(refresh)

        return Response(data, status=status.HTTP_200_OK)
