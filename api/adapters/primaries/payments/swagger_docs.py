from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi

list_payment_history_docs = swagger_auto_schema(
    operation_summary="Listar Historial de Pagos",
    operation_description=(
        "Este endpoint lista el historial de pagos realizados, con la opción de filtrar por rango de fechas."
    ),
    tags=["SPEI"],
    manual_parameters=[
        openapi.Parameter("limit", openapi.IN_QUERY, description="Número de resultados a devolver por página (paginación).", type=openapi.TYPE_INTEGER),
        openapi.Parameter("offset", openapi.IN_QUERY, description="Índice inicial desde el cual se devuelven los resultados (paginación).", type=openapi.TYPE_INTEGER),
        openapi.Parameter("defecha", openapi.IN_QUERY, description="Fecha inicial del periodo a consultar (YYYY-MM-DD).", type=openapi.FORMAT_DATE),
        openapi.Parameter("afecha", openapi.IN_QUERY, description="Fecha final del periodo a consultar (YYYY-MM-DD).", type=openapi.FORMAT_DATE),
    ],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Listado de pagos exitoso.",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "amount": openapi.Schema(type=openapi.TYPE_STRING, example="1500.50"),
                        "status": openapi.Schema(type=openapi.TYPE_STRING, example="completado"),
                        "row_id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                        "row_info": openapi.Schema(type=openapi.TYPE_STRING, example="Pago SPEI"),
                        "payment_date": openapi.Schema(type=openapi.FORMAT_DATE, example="2024-10-01"),
                        "pactivo": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                        "wactivo": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                        "scheduled_time": openapi.Schema(type=openapi.TYPE_STRING, example="12:00"),
                        "alias": openapi.Schema(type=openapi.TYPE_STRING, example="Pago de renta"),
                        "programed": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                        "creation_date": openapi.Schema(type=openapi.FORMAT_DATE, example="2024-09-25"),
                        "intension_date": openapi.Schema(type=openapi.FORMAT_DATE, example="2024-10-01"),
                        "reference": openapi.Schema(type=openapi.TYPE_STRING, example="123456789"),
                        "bank_institution": openapi.Schema(type=openapi.TYPE_STRING, example="BBVA"),
                        "num_account": openapi.Schema(type=openapi.TYPE_INTEGER, example=1234567890),
                        "comision": openapi.Schema(type=openapi.TYPE_NUMBER, example=10.00),
                        "IVA": openapi.Schema(type=openapi.TYPE_NUMBER, example=1.60),
                        "total": openapi.Schema(type=openapi.TYPE_NUMBER, example=11.60),
                        "RFC": openapi.Schema(type=openapi.TYPE_STRING, example="ABC123456789"),
                        "CURP": openapi.Schema(type=openapi.TYPE_STRING, example="ABCDE123456MEXXXX"),
                    },
                ),
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se encontraron pagos.",
        ),
    },
)


create_payment_docs = swagger_auto_schema(
    operation_summary="Generar un Pago a Terceros",
    operation_description=(
        "Este endpoint permite generar un nuevo pago a terceros, proporcionando los datos del destinatario "
        "y la cuenta desde la que se realizará el pago."
    ),
    tags=["SPEI"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["kauxiliar", "id_recipient", "id_account", "amount", "description", "payment_date", "reference", "payment_hour"],
        properties={
            "kauxiliar": openapi.Schema(type=openapi.TYPE_INTEGER, description="Código de la wallet asociada al pago.", example=44),
            "id_recipient": openapi.Schema(type=openapi.TYPE_INTEGER, description="Identificador del destinatario.", example=101),
            "id_account": openapi.Schema(type=openapi.TYPE_INTEGER, description="Identificador de la cuenta origen del pago.", example=5),
            "amount": openapi.Schema(type=openapi.TYPE_NUMBER, description="Monto del pago.", example=1500.50),
            "description": openapi.Schema(type=openapi.TYPE_STRING, description="Descripción del pago.", example="Pago de servicios"),
            "payment_date": openapi.Schema(type=openapi.FORMAT_DATE, description="Fecha del pago (YYYY-MM-DD).", example="2024-10-01"),
            "reference": openapi.Schema(type=openapi.TYPE_STRING, description="Referencia del pago.", example="123456789"),
            "payment_hour": openapi.Schema(type=openapi.TYPE_STRING, description="Hora programada del pago.", example="12:00"),
        },
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Pago generado exitosamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "kauxiliar": openapi.Schema(type=openapi.TYPE_INTEGER, example=44),
                    "id_recipient": openapi.Schema(type=openapi.TYPE_INTEGER, example=101),
                    "id_account": openapi.Schema(type=openapi.TYPE_INTEGER, example=5),
                    "amount": openapi.Schema(type=openapi.TYPE_NUMBER, example=1500.50),
                    "description": openapi.Schema(type=openapi.TYPE_STRING, example="Pago de servicios"),
                    "payment_date": openapi.Schema(type=openapi.FORMAT_DATE, example="2024-10-01"),
                    "reference": openapi.Schema(type=openapi.TYPE_STRING, example="123456789"),
                    "payment_hour": openapi.Schema(type=openapi.TYPE_STRING, example="12:00"),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se pudo generar el pago.",
        ),
    },
)

delete_payment_docs = swagger_auto_schema(
    operation_summary="Eliminar Pagos",
    operation_description=(
        "Este endpoint permite cancelar los pagos programados proporcionando el ID de la transacción."
    ),
    tags=["SPEI"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["id_transaction"],
        properties={
            "id_transaction": openapi.Schema(type=openapi.TYPE_INTEGER, description="Identificador de la transacción a cancelar.", example=1234),
        },
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Pago cancelado exitosamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id_transaction": openapi.Schema(type=openapi.TYPE_INTEGER, example=1234),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se pudo cancelar el pago.",
        ),
    },
)
