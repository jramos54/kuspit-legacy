from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi

create_recipient_wallet_docs = swagger_auto_schema(
    operation_summary="Crear una Wallet para un Destinatario",
    operation_description="Este endpoint permite crear una wallet (cuenta bancaria) para un destinatario.",
    tags=["Destinatarios"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["idcuenta", "institucion_bancaria", "cuenta", "catalogo_cuenta", "limite_operaciones", "is_active", "limite", "alias"],
        properties={
            "idcuenta": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID de la cuenta.", example=101),
            "institucion_bancaria": openapi.Schema(type=openapi.TYPE_STRING, description="Nombre del banco.", example="BBVA"),
            "cuenta": openapi.Schema(type=openapi.TYPE_STRING, description="Número de cuenta.", example="012345678901234567"),
            "catalogo_cuenta": openapi.Schema(type=openapi.TYPE_STRING, description="Tipo de cuenta.", example="debito"),
            "limite_operaciones": openapi.Schema(type=openapi.TYPE_INTEGER, description="Límite de operaciones.", example=10),
            "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Estado de la cuenta.", example=True),
            "limite": openapi.Schema(type=openapi.TYPE_INTEGER, description="Límite de la cuenta.", example=10000),
            "alias": openapi.Schema(type=openapi.TYPE_STRING, description="Alias de la cuenta.", example="Cuenta BBVA"),
        },
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Cuenta creada exitosamente.",
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se pudo crear la cuenta.",
        ),
    },
)

update_recipient_wallet_docs = swagger_auto_schema(
    operation_summary="Actualizar una Cuenta de Destinatario",
    operation_description="Este endpoint permite actualizar los datos de una cuenta bancaria (wallet) asociada a un destinatario.",
    tags=["Destinatarios"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["idcuenta", "limite_operaciones", "is_active", "limite", "alias"],
        properties={
            "idcuenta": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID de la cuenta.", example=29),
            "limite_operaciones": openapi.Schema(type=openapi.TYPE_INTEGER, description="Límite de operaciones.", example=9087),
            "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Estado de la cuenta.", example=False),
            "limite": openapi.Schema(type=openapi.TYPE_INTEGER, description="Límite de la cuenta.", example=1234),
            "alias": openapi.Schema(type=openapi.TYPE_STRING, description="Alias de la cuenta.", example="local"),
        },
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Cuenta actualizada exitosamente.",
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se pudo actualizar la cuenta.",
        ),
    },
)

delete_recipient_wallet_docs = swagger_auto_schema(
    operation_summary="Eliminar una Cuenta de Destinatario",
    operation_description="Este endpoint permite eliminar una cuenta bancaria (wallet) asociada a un destinatario.",
    tags=["Destinatarios"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["idcuenta", "iddestinatario"],
        properties={
            "idcuenta": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID de la cuenta a eliminar.", example=101),
            "iddestinatario": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID del destinatario asociado.", example=1),
        },
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Cuenta eliminada exitosamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "idcuenta": openapi.Schema(type=openapi.TYPE_INTEGER, example=101),
                    "iddestinatario": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se pudo eliminar la cuenta.",
        ),
    },
)

