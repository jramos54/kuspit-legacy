from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi

list_wallet_movements_historical_docs = swagger_auto_schema(
    operation_summary="Mostrar Histórico de Movimientos por Mes",
    operation_description=(
        "Este endpoint muestra la suma de los movimientos por mes para una wallet específica."
    ),
    tags=["Dashboard"],
    manual_parameters=[
        openapi.Parameter("limit", openapi.IN_QUERY, description="Número de resultados a devolver por página (paginación).", type=openapi.TYPE_INTEGER),
        openapi.Parameter("offset", openapi.IN_QUERY, description="Índice inicial desde el cual se devuelven los resultados (paginación).", type=openapi.TYPE_INTEGER),
        openapi.Parameter("kauxiliar", openapi.IN_QUERY, description="Código de la wallet que se quiere consultar.", type=openapi.TYPE_INTEGER),
    ],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Histórico de movimientos exitoso.",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "mes": openapi.Schema(type=openapi.TYPE_INTEGER, example=10),
                        "depositos": openapi.Schema(type=openapi.TYPE_STRING, example="5000.00"),
                        "retiros": openapi.Schema(type=openapi.TYPE_STRING, example="2000.00"),
                        "pago_servicios": openapi.Schema(type=openapi.TYPE_STRING, example="1000.00"),
                        "retiros_programados": openapi.Schema(type=openapi.TYPE_STRING, example="500.00"),
                        "current": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                    },
                ),
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se encontró histórico de movimientos para la wallet.",
        ),
    },
)
