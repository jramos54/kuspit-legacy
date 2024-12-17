from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status

list_banks_docs = swagger_auto_schema(
    operation_summary="Listar Bancos Disponibles",
    operation_description=(
        "Este endpoint permite obtener una lista de bancos disponibles. "
        "Se proporciona un catálogo de bancos, donde se puede buscar por nombre o identificar el banco mediante su CLABE. "
        "Esta funcionalidad es útil para los usuarios al momento de seleccionar un banco para transferencias o realizar configuraciones relacionadas con cuentas."
    ),
    tags=["Destinatarios"],
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
            "nombre",
            openapi.IN_QUERY,
            description=(
                "Nombre del banco o parte del nombre para realizar la búsqueda. "
                "Debe tener una longitud mínima de 1 carácter."
            ),
            type=openapi.TYPE_STRING,
        ),
        openapi.Parameter(
            "clabe",
            openapi.IN_QUERY,
            description=(
                "Cuenta CLABE para identificar el banco. "
                "Debe tener una longitud mínima de 1 carácter."
            ),
            type=openapi.TYPE_STRING,
        ),
    ],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="La solicitud se procesó correctamente y devuelve una lista de bancos que coinciden con los parámetros proporcionados.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "data": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "key": openapi.Schema(type=openapi.TYPE_INTEGER, example=301),
                                "nombre": openapi.Schema(type=openapi.TYPE_STRING, example="MEMBER_A"),
                            },
                        ),
                    ),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se encontraron bancos que coincidan con los criterios de búsqueda proporcionados.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING, example="No se encontro banco"),
                },
            ),
        ),
    },
)
