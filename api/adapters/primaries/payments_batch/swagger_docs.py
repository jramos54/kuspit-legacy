from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi

list_batch_payment_details_docs = swagger_auto_schema(
    operation_summary="Listar Detalle de Carga Masiva",
    operation_description=(
        "Este endpoint lista los detalles de la carga masiva de pagos, incluyendo los campos asociados a cada carga."
    ),
    tags=["SPEI"],
    manual_parameters=[
        openapi.Parameter("limit", openapi.IN_QUERY, description="Número de resultados a devolver por página (paginación).", type=openapi.TYPE_INTEGER),
        openapi.Parameter("offset", openapi.IN_QUERY, description="Índice inicial desde el cual se devuelven los resultados (paginación).", type=openapi.TYPE_INTEGER),
        openapi.Parameter("idarchivo", openapi.IN_QUERY, description="Identificador único del archivo cargado.", type=openapi.TYPE_INTEGER),
    ],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="El listado se ha generado con éxito.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Consulta del contenido del archivo exitosa"),
                    "data": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "idarchivo": openapi.Schema(type=openapi.TYPE_INTEGER, example=103),
                                "idpago": openapi.Schema(type=openapi.TYPE_INTEGER, example=35946),
                                "institucion_contraparte": openapi.Schema(type=openapi.TYPE_STRING, example="40012"),
                                "monto": openapi.Schema(type=openapi.TYPE_STRING, example="9.43"),
                                "nombre_beneficiario": openapi.Schema(type=openapi.TYPE_STRING, example="Gail Rios"),
                                "tipo_cuenta_beneficiario": openapi.Schema(type=openapi.TYPE_STRING, example="40"),
                                "cuenta_beneficiario": openapi.Schema(type=openapi.TYPE_STRING, example="012029356121531544"),
                                "concepto_pago": openapi.Schema(type=openapi.TYPE_STRING, example="Issue into what fast."),
                                "referencia_numerica": openapi.Schema(type=openapi.TYPE_STRING, example="751102"),
                                "idtransaccion": openapi.Schema(type=openapi.TYPE_STRING, example=None),
                                "comision": openapi.Schema(type=openapi.TYPE_STRING, example=None),
                                "fecha_real": openapi.Schema(type=openapi.TYPE_STRING, example=None),
                            },
                        ),
                    ),
                },
            ),
        ),
        status.HTTP_403_FORBIDDEN: openapi.Response(
            description="No se encontraron resultados.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING, example="{'non_field_errors': [ErrorDetail(string='No data provided', code='null')]}"),
                    "data": openapi.Schema(type=openapi.TYPE_STRING, example=""),
                },
            ),
        ),
    },
)

apply_batch_payment_docs = swagger_auto_schema(
    operation_summary="Aplicar Datos de la Carga Masiva",
    operation_description="Este endpoint permite aplicar los datos de un archivo cargado de manera masiva.",
    tags=["SPEI"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["idarchivo"],
        properties={
            "idarchivo": openapi.Schema(type=openapi.TYPE_INTEGER, description="Identificador del archivo cargado.", example=103),
        },
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Los datos se han aplicado correctamente.",
        ),
        status.HTTP_403_FORBIDDEN: openapi.Response(
            description="No se pudieron aplicar los datos.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Error al aplicar las cargas masivas"),
                    "data": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "status": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                            "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Error: El saldo no es suficiente para realizar la transaccion"),
                        },
                    ),
                },
            ),
        ),
    },
)

get_batch_progress_docs = swagger_auto_schema(
    method='get',
    operation_summary="Obtener Progreso de la Carga de Archivo",
    operation_description="Este endpoint permite consultar el progreso del procesamiento de un archivo cargado.",
    tags=["SPEI"],
    manual_parameters=[
        openapi.Parameter("task_id", openapi.IN_PATH, description="Identificador único de la tarea de carga masiva.", type=openapi.TYPE_STRING),
    ],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="El progreso del archivo se muestra correctamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(type=openapi.TYPE_STRING, example="Proceso de carga a OpenFin terminado"),
                    "data": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "_id": openapi.Schema(type=openapi.TYPE_INTEGER, example=110),
                            "Archivo": openapi.Schema(type=openapi.TYPE_STRING, example="temp_da038b73-376f-4a1d-8307-08fcd5c8222d_pagos_1.csv"),
                            "Fecha Carga": openapi.Schema(type=openapi.TYPE_STRING, example="2024-10-09"),
                            "Fecha Pago": openapi.Schema(type=openapi.TYPE_STRING, example=None),
                            "Hora Pago": openapi.Schema(type=openapi.TYPE_STRING, example="N/A"),
                            "Aplicado": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                            "Acción": openapi.Schema(type=openapi.TYPE_STRING, example=""),
                        },
                    ),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="El task_id no se encontró.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING, example="Final message not found or is empty."),
                },
            ),
        ),
    },
)

list_uploaded_files_docs = swagger_auto_schema(
    operation_summary="Listar Archivos Cargados por el Usuario",
    operation_description="Este endpoint lista todos los archivos que el usuario ha cargado en la plataforma para la carga masiva de pagos.",
    tags=["SPEI"],
    manual_parameters=[
        openapi.Parameter("limit", openapi.IN_QUERY, description="Número de resultados a devolver por página (paginación).", type=openapi.TYPE_INTEGER),
        openapi.Parameter("offset", openapi.IN_QUERY, description="Índice inicial desde el cual se devuelven los resultados (paginación).", type=openapi.TYPE_INTEGER),
        openapi.Parameter("kauxiliar", openapi.IN_QUERY, description="Wallet del usuario donde se efectúa la carga masiva.", type=openapi.TYPE_INTEGER),
    ],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="El listado de archivos se ha generado con éxito.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Consulta de Archivos exitosa"),
                    "data": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "_id": openapi.Schema(type=openapi.TYPE_INTEGER, example=106),
                                "Archivo": openapi.Schema(type=openapi.TYPE_STRING, example="temp_db859918-64f1-4c76-85b8-2e475992df96_pagos_1.csv"),
                                "Aplicado": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                            },
                        ),
                    ),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se encontraron archivos cargados.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING, example="{'non_field_errors': [ErrorDetail(string='No data provided', code='null')]}"),
                    "data": openapi.Schema(type=openapi.TYPE_STRING, example=""),
                },
            ),
        ),
    },
)

upload_batch_payment_file_docs = swagger_auto_schema(
    operation_summary="Carga Masiva de Pagos (Subir Archivo)",
    operation_description="Este endpoint permite cargar un archivo CSV que contiene los datos para la carga masiva de pagos.",
    tags=["SPEI"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["file", "kauxiliar"],
        properties={
            "file": openapi.Schema(type=openapi.TYPE_STRING, description="Archivo CSV que será cargado para el proceso de pagos.", example="pagos.csv"),
            "kauxiliar": openapi.Schema(type=openapi.TYPE_INTEGER, description="Wallet del usuario donde se efectúa la carga masiva.", example=44),
        },
    ),
    responses={
        status.HTTP_202_ACCEPTED: openapi.Response(
            description="El archivo ha sido recibido y está siendo procesado.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "task_id": openapi.Schema(type=openapi.TYPE_STRING, example="da038b73-376f-4a1d-8307-08fcd5c8222d"),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="Error al recibir o procesar el archivo.",
        ),
    },
)
