from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi

login_docs = swagger_auto_schema(
    operation_summary="Iniciar Sesión (Login)",
    operation_description=(
        "Este endpoint toma un conjunto de credenciales de usuario (correo electrónico y contraseña) "
        "y devuelve un par de tokens JSON web (access y refresh) para probar la autenticación de dichas credenciales."
    ),
    tags=["Seguridad"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["email", "password"],
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING, description="Correo electrónico del usuario.", example="user@example.com"),
            "password": openapi.Schema(type=openapi.TYPE_STRING, description="Contraseña del usuario.", example="password123"),
        },
    ),
    responses={
        status.HTTP_201_CREATED: openapi.Response(
            description="Autenticación exitosa, se devuelven los tokens de acceso y refresh.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "access": openapi.Schema(type=openapi.TYPE_STRING, example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."),
                    "refresh": openapi.Schema(type=openapi.TYPE_STRING, example="dGVzdC5yZWZyZXNoLnRva2VuLmhlcmUuLi4"),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="Las credenciales proporcionadas no son válidas.",
        ),
    },
)

logout_docs = swagger_auto_schema(
    operation_summary="Cerrar Sesión (Logout)",
    operation_description=(
        "Este endpoint toma el token de refresco (refresh token) y lo invalida, cerrando la sesión del usuario."
    ),
    tags=["Seguridad"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["refresh"],
        properties={
            "refresh": openapi.Schema(type=openapi.TYPE_STRING, description="Token de refresco proporcionado.", example="dGVzdC5yZWZyZXNoLnRva2VuLmhlcmUuLi4"),
        },
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Cierre de sesión exitoso, el token de refresco ha sido invalidado.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Cierre de sesión exitoso."),
                },
            ),
        ),
        status.HTTP_401_UNAUTHORIZED: openapi.Response(
            description="El token de refresco proporcionado no es válido o ya ha sido invalidado.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Given token not valid for any token type"),
                    "code": openapi.Schema(type=openapi.TYPE_STRING, example="token_not_valid"),
                    "messages": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "token_class": openapi.Schema(type=openapi.TYPE_STRING, example="AccessToken"),
                                "token_type": openapi.Schema(type=openapi.TYPE_STRING, example="access"),
                                "message": openapi.Schema(type=openapi.TYPE_STRING, example="Token is invalid or expired"),
                            },
                        ),
                    ),
                },
            ),
        ),
    },
)

token_refresh_docs = swagger_auto_schema(
    operation_summary="Refrescar Token (Token Refresh)",
    operation_description=(
        "Este endpoint toma un token de refresco (refresh token) y devuelve un nuevo token de acceso (access token) "
        "para que el usuario continúe autenticado sin necesidad de volver a ingresar sus credenciales."
    ),
    tags=["Seguridad"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["refresh"],
        properties={
            "refresh": openapi.Schema(type=openapi.TYPE_STRING, description="Token de refresco proporcionado.", example="dGVzdC5yZWZyZXNoLnRva2VuLmhlcmUuLi4"),
        },
    ),
    responses={
        status.HTTP_201_CREATED: openapi.Response(
            description="Token de acceso renovado exitosamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "access": openapi.Schema(type=openapi.TYPE_STRING, example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."),
                    "refresh": openapi.Schema(type=openapi.TYPE_STRING, example="dGVzdC5yZWZyZXNoLnRva2VuLmhlcmUuLi4"),
                },
            ),
        ),
    },
)
