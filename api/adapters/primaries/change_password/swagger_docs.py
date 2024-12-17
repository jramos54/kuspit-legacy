from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status

cambiar_password_docs = swagger_auto_schema(
    operation_summary="Cambio de Contraseña",
    operation_description="Servicio para cambio de contraseña por parte del usuario.",
    tags=["Configuración"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["old_password", "new_password", "password_confirmation"],
        properties={
            "old_password": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Contraseña actual del usuario.",
                example="password123"
            ),
            "new_password": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Nueva contraseña que el usuario desea establecer.",
                example="newpassword123"
            ),
            "password_confirmation": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Confirmación de la nueva contraseña.",
                example="newpassword123"
            ),
        },
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Contraseña cambiada exitosamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Password cambiado exitosamente"),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="Usuario no encontrado.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Usuario no encontrado."),
                },
            ),
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description="Error en la solicitud.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Error en la validación de datos."),
                },
            ),
        ),
    },
)
