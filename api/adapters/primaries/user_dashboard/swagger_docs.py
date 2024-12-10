from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi

show_user_data_docs = swagger_auto_schema(
    operation_summary="Mostrar Datos del Usuario",
    operation_description=(
        "Este endpoint muestra los datos del usuario autenticado, incluidos el nombre, correo, perfil y el estado del 2FA."
    ),
    tags=["Dashboard"],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Datos del usuario obtenidos exitosamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Consulta de usuario exitosa"),
                    "data": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "nombre": openapi.Schema(type=openapi.TYPE_STRING, example="Luis Jarero Martinez"),
                            "correo": openapi.Schema(type=openapi.TYPE_STRING, example="luis.jarero@kuspit.com"),
                            "kasociado": openapi.Schema(type=openapi.TYPE_INTEGER, example=98),
                            "perfil": openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(type=openapi.TYPE_STRING, example="dypfe_superuser"),
                            ),
                            "status_2fa": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                        },
                    ),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="Usuario no encontrado.",
        ),
    },
)

get_user_by_email_docs = swagger_auto_schema(
    operation_summary="Obtener Nombre de Usuario por Correo",
    operation_description=(
        "Este endpoint muestra el nombre de usuario dado a un correo electrónico. No requiere autenticación."
    ),
    tags=["Dashboard"],
    manual_parameters=[
        openapi.Parameter(
            "email",
            openapi.IN_QUERY,
            description="Correo electrónico de consulta.",
            type=openapi.TYPE_STRING,
        ),
    ],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Nombre del usuario obtenido exitosamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "email": openapi.Schema(type=openapi.TYPE_STRING, example="barry.allen.kuspit@gmail.com"),
                    "full_name": openapi.Schema(type=openapi.TYPE_STRING, example="Barry Allen"),
                    "is_new_user": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                    "status_2fa": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="Usuario no encontrado.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Not found."),
                },
            ),
        ),
    },
)

update_new_user_status_docs = swagger_auto_schema(
    operation_summary="Actualizar Estado de Nuevo Usuario",
    operation_description="Este endpoint cambia el estado de si el usuario es nuevo o no. No requiere autenticación.",
    tags=["Seguridad"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["email"],
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING, description="Correo electrónico de consulta.", example="joel.ramos@kuspit.com"),
        },
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Estado del usuario actualizado exitosamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "email": openapi.Schema(type=openapi.TYPE_STRING, example="joel.ramos@kuspit.com"),
                    "full_name": openapi.Schema(type=openapi.TYPE_STRING, example="Joel Ramos"),
                    "is_new_user": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                },
            ),
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description="Correo electrónico requerido.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Email is required"),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="Usuario no encontrado.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Not found."),
                },
            ),
        ),
    },
)

update_2fa_status_docs = swagger_auto_schema(
    operation_summary="Actualizar Estado del 2FA",
    operation_description="Este endpoint permite cambiar el estado del 2FA (autenticación de dos factores) para el usuario.",
    tags=["Seguridad"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["status_2fa"],
        properties={
            "status_2fa": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Nuevo estado del 2FA.", example=True),
        },
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Estado del 2FA actualizado exitosamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Actualización de status 2FA exitosa"),
                    "data": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "nombre": openapi.Schema(type=openapi.TYPE_STRING, example="Luis Jarero Martinez"),
                            "correo": openapi.Schema(type=openapi.TYPE_STRING, example="luis.jarero@kuspit.com"),
                            "kasociado": openapi.Schema(type=openapi.TYPE_INTEGER, example=98),
                            "perfil": openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(type=openapi.TYPE_STRING, example="dypfe_superuser"),
                            ),
                            "status_2fa": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                        },
                    ),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="Usuario no encontrado.",
        ),
    },
)
