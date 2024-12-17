from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi

list_batch_recipients_docs = swagger_auto_schema(
    operation_summary="Listar Detalle de Carga Masiva de Destinatarios",
    operation_description=(
        "Este endpoint lista los detalles de las cargas masivas realizadas para los destinatarios, mostrando información relevante de los archivos cargados."
    ),
    tags=["Destinatarios"],
    manual_parameters=[
        openapi.Parameter("limit", openapi.IN_QUERY, description="Número de resultados a devolver por página (paginación).", type=openapi.TYPE_INTEGER),
        openapi.Parameter("offset", openapi.IN_QUERY, description="Índice inicial desde el cual se devuelven los resultados (paginación).", type=openapi.TYPE_INTEGER),
        openapi.Parameter("id", openapi.IN_QUERY, description="Identificador del archivo cargado.", type=openapi.TYPE_INTEGER),
    ],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Listado exitoso de los detalles de la carga masiva.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Consulta del contenido del archivo exitosa"),
                    "data": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "idarchivo": openapi.Schema(type=openapi.TYPE_INTEGER, example=67),
                                "idregistro": openapi.Schema(type=openapi.TYPE_INTEGER, example=159),
                                "nombre": openapi.Schema(type=openapi.TYPE_STRING, example="Denise Smith"),
                                "tipo_persona": openapi.Schema(type=openapi.TYPE_STRING, example="FISICA"),
                                "rfc": openapi.Schema(type=openapi.TYPE_STRING, example="KIWM3507102AV"),
                                "alias": openapi.Schema(type=openapi.TYPE_STRING, example="torreselizabeth"),
                                "institucion": openapi.Schema(type=openapi.TYPE_STRING, example="40021"),
                                "tipo_cuenta_beneficiario": openapi.Schema(type=openapi.TYPE_STRING, example="40"),
                                "cuenta_beneficiario": openapi.Schema(type=openapi.TYPE_STRING, example="021276915619796419"),
                                "limite_operacion": openapi.Schema(type=openapi.TYPE_STRING, example="36933.00"),
                                "numero_operaciones": openapi.Schema(type=openapi.TYPE_INTEGER, example=37),
                                "email": openapi.Schema(type=openapi.TYPE_STRING, example="andre45@example.com"),
                                "fecha_real": openapi.Schema(type=openapi.TYPE_STRING, example="27/09/2024 12:03:08.276251 CST"),
                                "idbeneficiario": openapi.Schema(type=openapi.TYPE_INTEGER, example=183),
                                "msg": openapi.Schema(type=openapi.TYPE_STRING, example=None),
                            },
                        ),
                    ),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se encontraron registros.",
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

apply_batch_recipients_docs = swagger_auto_schema(
    operation_summary="Aplicar Datos de la Carga Masiva de Destinatarios",
    operation_description="Este endpoint permite aplicar los datos cargados de manera masiva para los destinatarios.",
    tags=["Destinatarios"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["id"],
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Identificador del archivo cargado.", example=67),
        },
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Datos aplicados correctamente.",
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se pudo aplicar el archivo.",
        ),
    },
)

delete_batch_recipient_file_docs = swagger_auto_schema(
    operation_summary="Eliminar un Archivo Cargado",
    operation_description="Este endpoint permite eliminar un archivo cargado previamente.",
    tags=["Destinatarios"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["id"],
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Identificador del archivo cargado.", example=67),
        },
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Archivo eliminado con éxito.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Se elimino correctamente el archivo"),
                    "data": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "status": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                            "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Se eliminó la importación correctamente"),
                        },
                    ),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="El archivo no se pudo encontrar o eliminar.",
        ),
    },
)

get_recipient_batch_progress_docs = swagger_auto_schema(
    method="get",
    operation_summary="Obtener Progreso de la Carga de Archivo de Destinatarios",
    operation_description="Este endpoint permite consultar el progreso de un archivo cargado en la plataforma.",
    tags=["Destinatarios"],
    manual_parameters=[
        openapi.Parameter("task_id", openapi.IN_PATH, description="Identificador único de la tarea de procesamiento.", type=openapi.TYPE_STRING),
    ],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Progreso del archivo obtenido exitosamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "message": openapi.Schema(type=openapi.TYPE_STRING, example="Proceso de carga a OpenFin terminado"),
                    "data": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "Id": openapi.Schema(type=openapi.TYPE_INTEGER, example=72),
                            "Archivo": openapi.Schema(type=openapi.TYPE_STRING, example="temp_c7174413-8766-49e7-9462-fd3e5a1b6c9c_destinatarios_1000.csv"),
                            "Fecha": openapi.Schema(type=openapi.TYPE_STRING, example="09/10/2024"),
                            "Cargado por": openapi.Schema(type=openapi.TYPE_STRING, example="jacob.munoz@kuspit.com"),
                            "Aplicado": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                            "Acción": openapi.Schema(type=openapi.TYPE_STRING, example=""),
                        },
                    ),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="Task ID no encontrado.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING, example="Final message not found or is empty."),
                },
            ),
        ),
    },
)

list_uploaded_recipient_files_docs = swagger_auto_schema(
    operation_summary="Listar Archivos Cargados por el Usuario",
    operation_description="Este endpoint lista todos los archivos que el usuario ha cargado en la plataforma para la carga masiva de destinatarios.",
    tags=["Destinatarios"],
    manual_parameters=[
        openapi.Parameter("limit", openapi.IN_QUERY, description="Número de resultados a devolver por página (paginación).", type=openapi.TYPE_INTEGER),
        openapi.Parameter("offset", openapi.IN_QUERY, description="Índice inicial desde el cual se devuelven los resultados (paginación).", type=openapi.TYPE_INTEGER),
    ],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Listado de archivos exitoso.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Consulta de Archivos exitosa"),
                    "data": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "Id": openapi.Schema(type=openapi.TYPE_INTEGER, example=69),
                                "Archivo": openapi.Schema(type=openapi.TYPE_STRING, example="temp_d9810f0f-6d17-4265-8e39-1462a2d4e0dd_masiva_1.csv"),
                                "Fecha": openapi.Schema(type=openapi.TYPE_STRING, example="09/10/2024"),
                                "Aplicado": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                            },
                        ),
                    ),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se encontraron archivos cargados.",
        ),
    },
)

upload_recipient_batch_file_docs = swagger_auto_schema(
    operation_summary="Carga Masiva de Destinatarios (Subir Archivo)",
    operation_description="Este endpoint permite cargar un archivo CSV con los datos de destinatarios para ser procesados de manera masiva.",
    tags=["Destinatarios"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["file"],
        properties={
            "file": openapi.Schema(type=openapi.TYPE_STRING, description="Archivo CSV con los datos de destinatarios.", example="destinatarios.csv"),
        },
    ),
    responses={
        status.HTTP_202_ACCEPTED: openapi.Response(
            description="El archivo ha sido recibido y está en proceso.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "task_id": openapi.Schema(type=openapi.TYPE_STRING, example="a8cd34b0-289d-44f0-857f-942085bfbb7a"),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se pudo procesar el archivo.",
        ),
    },
)
