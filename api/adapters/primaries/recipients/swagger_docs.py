from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi

list_recipients_docs = swagger_auto_schema(
    operation_summary="Listar Destinatarios",
    operation_description=(
        "Este endpoint lista todos los destinatarios registrados en la cuenta, junto con sus datos personales y las cuentas asociadas."
    ),
    tags=["Destinatarios"],
    manual_parameters=[
        openapi.Parameter("limit", openapi.IN_QUERY, description="Número de resultados a devolver por página (paginación).", type=openapi.TYPE_INTEGER),
        openapi.Parameter("offset", openapi.IN_QUERY, description="Índice inicial desde el cual se devuelven los resultados (paginación).", type=openapi.TYPE_INTEGER),
    ],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Listado de destinatarios exitoso.",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "iddestinatario": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                        "nombre": openapi.Schema(type=openapi.TYPE_STRING, example="Juan"),
                        "paterno": openapi.Schema(type=openapi.TYPE_STRING, example="Pérez"),
                        "materno": openapi.Schema(type=openapi.TYPE_STRING, example="García"),
                        "rfc": openapi.Schema(type=openapi.TYPE_STRING, example="PERJ850101HMCRRL09"),
                        "curp": openapi.Schema(type=openapi.TYPE_STRING, example="PERJ850101HDFRLL09"),
                        "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                        "correo": openapi.Schema(type=openapi.TYPE_STRING, example="juan.perez@example.com"),
                        "pfisica": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                        "cuentas": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "idcuenta": openapi.Schema(type=openapi.TYPE_INTEGER, example=101),
                                    "institucion_bancaria": openapi.Schema(type=openapi.TYPE_STRING, example="BBVA"),
                                    "cuenta": openapi.Schema(type=openapi.TYPE_STRING, example="012345678901234567"),
                                    "catalogo_cuenta": openapi.Schema(type=openapi.TYPE_STRING, example="debito"),
                                    "limite_operaciones": openapi.Schema(type=openapi.TYPE_INTEGER, example=10),
                                    "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                                    "limite": openapi.Schema(type=openapi.TYPE_INTEGER, example=10000),
                                    "alias": openapi.Schema(type=openapi.TYPE_STRING, example="Cuenta BBVA"),
                                },
                            ),
                        ),
                    },
                ),
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se encontraron destinatarios.",
        ),
    },
)

create_recipient_docs = swagger_auto_schema(
    operation_summary="Crear un Nuevo Destinatario",
    operation_description="Este endpoint permite registrar un nuevo destinatario en la cuenta.",
    tags=["Destinatarios"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["nombre", "paterno", "correo", "pfisica"],
        properties={
            "nombre": openapi.Schema(type=openapi.TYPE_STRING, description="Nombre del destinatario.", example="Pedro"),
            "paterno": openapi.Schema(type=openapi.TYPE_STRING, description="Apellido paterno del destinatario.", example="López"),
            "materno": openapi.Schema(type=openapi.TYPE_STRING, description="Apellido materno del destinatario.", example="Ramírez"),
            "rfc": openapi.Schema(type=openapi.TYPE_STRING, description="RFC del destinatario.", example="LOPR850101HMCRRL09"),
            "curp": openapi.Schema(type=openapi.TYPE_STRING, description="CURP del destinatario.", example="LOPR850101HDFRLL09"),
            "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Indica si el destinatario está activo.", example=True),
            "correo": openapi.Schema(type=openapi.TYPE_STRING, description="Correo electrónico del destinatario.", example="pedro.lopez@example.com"),
            "pfisica": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Indica si el destinatario es una persona física.", example=True),
        },
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Destinatario creado exitosamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "iddestinatario": openapi.Schema(type=openapi.TYPE_INTEGER, example=2),
                    "nombre": openapi.Schema(type=openapi.TYPE_STRING, example="Pedro"),
                    "paterno": openapi.Schema(type=openapi.TYPE_STRING, example="López"),
                    "materno": openapi.Schema(type=openapi.TYPE_STRING, example="Ramírez"),
                    "rfc": openapi.Schema(type=openapi.TYPE_STRING, example="LOPR850101HMCRRL09"),
                    "curp": openapi.Schema(type=openapi.TYPE_STRING, example="LOPR850101HDFRLL09"),
                    "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                    "correo": openapi.Schema(type=openapi.TYPE_STRING, example="pedro.lopez@example.com"),
                    "pfisica": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se pudo crear el destinatario.",
        ),
    },
)

update_recipient_docs = swagger_auto_schema(
    operation_summary="Actualizar un Destinatario Existente",
    operation_description="Este endpoint permite actualizar los datos de un destinatario existente.",
    tags=["Destinatarios"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["iddestinatario", "nombre", "paterno", "correo", "pfisica"],
        properties={
            "iddestinatario": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID del destinatario.", example=2),
            "nombre": openapi.Schema(type=openapi.TYPE_STRING, description="Nombre del destinatario.", example="Pedro"),
            "paterno": openapi.Schema(type=openapi.TYPE_STRING, description="Apellido paterno del destinatario.", example="López"),
            "materno": openapi.Schema(type=openapi.TYPE_STRING, description="Apellido materno del destinatario.", example="Ramírez"),
            "rfc": openapi.Schema(type=openapi.TYPE_STRING, description="RFC del destinatario.", example="LOPR850101HMCRRL09"),
            "curp": openapi.Schema(type=openapi.TYPE_STRING, description="CURP del destinatario.", example="LOPR850101HDFRLL09"),
            "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Indica si el destinatario está activo.", example=True),
            "correo": openapi.Schema(type=openapi.TYPE_STRING, description="Correo electrónico del destinatario.", example="pedro.lopez@example.com"),
            "pfisica": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Indica si el destinatario es una persona física.", example=True),
        },
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Destinatario actualizado exitosamente.",
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se pudo actualizar el destinatario.",
        ),
    },
)

delete_recipient_docs = swagger_auto_schema(
    operation_summary="Eliminar un Destinatario",
    operation_description="Este endpoint permite eliminar un destinatario existente de la cuenta.",
    tags=["Destinatarios"],
    manual_parameters=[
        openapi.Parameter("iddestinatario", openapi.IN_QUERY, description="Identificador del destinatario que se desea eliminar.", type=openapi.TYPE_INTEGER),
    ],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Destinatario eliminado exitosamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "iddestinatario": openapi.Schema(type=openapi.TYPE_INTEGER, example=2),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se pudo eliminar el destinatario.",
        ),
    },
)
