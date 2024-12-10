from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi

list_wallet_types_docs = swagger_auto_schema(
    operation_summary="Listar Tipos de Wallet Disponibles",
    operation_description=(
        "Este endpoint lista el catálogo de los diferentes tipos de wallet (productos) disponibles en la plataforma."
    ),
    tags=["Configuración"],
    manual_parameters=[
        openapi.Parameter(
            "limit",
            openapi.IN_QUERY,
            description="Número de resultados a devolver por página (paginación).",
            type=openapi.TYPE_INTEGER,
        ),
        openapi.Parameter(
            "offset",
            openapi.IN_QUERY,
            description="Índice inicial desde el cual se devuelven los resultados (paginación).",
            type=openapi.TYPE_INTEGER,
        ),
        openapi.Parameter(
            "idproducto",
            openapi.IN_QUERY,
            description="Identificador único del tipo de wallet (producto) que se desea consultar.",
            type=openapi.TYPE_INTEGER,
        ),
    ],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Listado de productos exitoso.",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "idproducto": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                        "nombre": openapi.Schema(type=openapi.TYPE_STRING, example="Wallet Personal"),
                    },
                ),
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se encontraron productos.",
        ),
    },
)
