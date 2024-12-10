from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi
from . import accounts_serializers 

list_wallets_docs = swagger_auto_schema(
    operation_summary="Listar Wallets de la Cuenta del Usuario",
    operation_description=(
        "Este endpoint permite listar las wallets asociadas a la cuenta del usuario. "
        "Las wallets se utilizan para enviar o recibir recursos. "
        "El usuario autenticado puede ver todas las wallets que se encuentran vinculadas a su cuenta, "
        "junto con detalles relevantes de cada una."
    ),
    tags=["Dashboard"],
    manual_parameters=[
        openapi.Parameter(
            "limit",
            openapi.IN_QUERY,
            description="Número de resultados a devolver por página.",
            type=openapi.TYPE_INTEGER,
        ),
        openapi.Parameter(
            "offset",
            openapi.IN_QUERY,
            description="Índice inicial desde el cual se devuelven los resultados.",
            type=openapi.TYPE_INTEGER,
        ),
        openapi.Parameter(
            "kauxiliar",
            openapi.IN_QUERY,
            description="Parámetro auxiliar (propósito específico definido en el contexto de la aplicación).",
            type=openapi.TYPE_INTEGER,
        ),
    ],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="La solicitud se procesó correctamente y devuelve una lista de wallets asociadas al usuario.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Wallets disponibles"),
                    "data": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "alias": openapi.Schema(type=openapi.TYPE_STRING, example="wallet 1"),
                                "clabe": openapi.Schema(type=openapi.TYPE_STRING, example="729180000000000052"),
                                "activo": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                                "saldo": openapi.Schema(type=openapi.TYPE_NUMBER, example=0.0),
                                "kauxiliar": openapi.Schema(type=openapi.TYPE_INTEGER, example=44),
                            },
                        ),
                    ),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se encontraron wallets asociadas para el usuario.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING, example="No se encontraron cuentas asociadas al usuario."),
                },
            ),
        ),
    }
)

create_account_docs = swagger_auto_schema(
    operation_summary="Crear una Nueva Wallet",
    operation_description=(
        "Este endpoint permite la creación de una nueva wallet asociada al usuario autenticado. "
        "La wallet puede ser utilizada para gestionar fondos y realizar transacciones."
    ),
    tags=["Configuración"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["alias", "type_account"],
        properties={
            "alias": openapi.Schema(
                type=openapi.TYPE_STRING,
                description=(
                    "El alias o nombre asignado a la wallet. Este campo permite al usuario identificar "
                    "fácilmente la wallet entre varias cuentas. Debe ser único por usuario y tener un "
                    "significado claro para facilitar su reconocimiento."
                ),
                example="Nueva Wallet Personal",
            ),
            "type_account": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description=(
                    "Representa el tipo de cuenta asociado con la wallet. Este valor es un código numérico "
                    "que corresponde a diferentes tipos de cuentas definidos por el sistema, como cuentas "
                    "de ahorro, cuentas corrientes, cuentas empresariales, etc."
                ),
                example=2001,
            ),
        },
    ),
    responses={
        status.HTTP_201_CREATED: openapi.Response(
            description="La wallet se ha creado satisfactoriamente y se devuelve la información de la misma.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="La cuenta se ha creado exitosamente",
                    ),
                    "data": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "alias": openapi.Schema(
                                type=openapi.TYPE_STRING, example="Nueva Wallet Personal"
                            ),
                            "type_account": openapi.Schema(
                                type=openapi.TYPE_INTEGER, example=2001
                            ),
                        },
                    ),
                },
            ),
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description="No se pudo crear la wallet debido a un error (p. ej., problemas de validación o restricciones).",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="No se pudo crear la cuenta. Verifique los datos enviados.",
                    ),
                    "data": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        description="Información parcial o errónea proporcionada durante la creación de la wallet.",
                        properties={
                            "alias": openapi.Schema(
                                type=openapi.TYPE_STRING, example="Nombre inválido"
                            ),
                            "type_account": openapi.Schema(
                                type=openapi.TYPE_INTEGER, example=None
                            ),
                        },
                    ),
                },
            ),
        ),
    },
)

