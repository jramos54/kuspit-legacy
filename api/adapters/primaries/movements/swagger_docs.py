from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi

list_wallet_movements_docs = swagger_auto_schema(
    operation_summary="Listar Movimientos de una Wallet",
    operation_description=(
        "Este endpoint lista los movimientos asociados a una wallet específica. "
        "Los movimientos pueden filtrarse por tipo de movimiento, estatus y rango de fechas."
    ),
    tags=["Dashboard"],
    manual_parameters=[
        openapi.Parameter("limit", openapi.IN_QUERY, description="Número de resultados a devolver por página (paginación).", type=openapi.TYPE_INTEGER),
        openapi.Parameter("offset", openapi.IN_QUERY, description="Índice inicial desde el cual se devuelven los resultados (paginación).", type=openapi.TYPE_INTEGER),
        openapi.Parameter("kauxiliar", openapi.IN_QUERY, description="Código de la wallet que se quiere consultar.", type=openapi.TYPE_INTEGER),
        openapi.Parameter("defecha", openapi.IN_QUERY, description="Fecha inicial del periodo a consultar (YYYY-MM-DD).", type=openapi.FORMAT_DATE),
        openapi.Parameter("afecha", openapi.IN_QUERY, description="Fecha final del periodo a consultar (YYYY-MM-DD).", type=openapi.FORMAT_DATE),
        openapi.Parameter("limite", openapi.IN_QUERY, description="Número máximo de movimientos a mostrar.", type=openapi.TYPE_INTEGER),
        openapi.Parameter("movimiento", openapi.IN_QUERY, description="Tipo de movimiento a filtrar (depósitos, retiros, etc.).", type=openapi.TYPE_STRING),
        openapi.Parameter("estatus", openapi.IN_QUERY, description="Estatus de los movimientos a filtrar (pendiente, completado, etc.).", type=openapi.TYPE_STRING),
    ],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Listado de movimientos exitoso.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Consulta de movimientos exitosa"),
                    "data": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "fecha_elaboracion": openapi.Schema(type=openapi.FORMAT_DATE, example="2024-10-09"),
                                "fecha_pago": openapi.Schema(type=openapi.FORMAT_DATE, example="2024-01-01"),
                                "movimiento": openapi.Schema(type=openapi.TYPE_STRING, example="Retiro"),
                                "estatus": openapi.Schema(type=openapi.TYPE_STRING, example="Pendiente"),
                                "destinatario": openapi.Schema(type=openapi.TYPE_STRING, example="Mary Banks"),
                                "cuenta_bancaria": openapi.Schema(type=openapi.TYPE_STRING, example="002553181937661452"),
                                "monto": openapi.Schema(type=openapi.TYPE_NUMBER, example=-717.59),
                                "concepto": openapi.Schema(type=openapi.TYPE_STRING, example="accumsan tinciduntd vivamus"),
                                "clave_rastreo": openapi.Schema(type=openapi.TYPE_STRING, example=None),
                                "referencia": openapi.Schema(type=openapi.TYPE_STRING, example="ante4414"),
                                "info": openapi.Schema(type=openapi.TYPE_STRING, example="???"),
                                "pfisica": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                                "institucion_bancaria": openapi.Schema(type=openapi.TYPE_STRING, example="BANAMEX"),
                            },
                        ),
                    ),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se encontraron movimientos para la wallet.",
        ),
    },
)
