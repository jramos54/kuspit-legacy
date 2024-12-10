from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi

list_operators_docs = swagger_auto_schema(
    operation_summary="Listar Operadores y sus Roles",
    operation_description=(
        "Este endpoint lista los operadores registrados en la cuenta, permitiendo obtener información sobre "
        "su nombre, correo electrónico, roles y permisos asignados."
    ),
    tags=["Configuración"],
    manual_parameters=[
        openapi.Parameter("limit", openapi.IN_QUERY, description="Número de resultados a devolver por página (paginación).", type=openapi.TYPE_INTEGER),
        openapi.Parameter("offset", openapi.IN_QUERY, description="Índice inicial desde el cual se devuelven los resultados (paginación).", type=openapi.TYPE_INTEGER),
    ],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Listado exitoso de los operadores.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Consulta de operadores exitosa"),
                    "data": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "idoperador": openapi.Schema(type=openapi.TYPE_INTEGER, example=42),
                                "kasociado": openapi.Schema(type=openapi.TYPE_INTEGER, example=72),
                                "nombre": openapi.Schema(type=openapi.TYPE_STRING, example="fulanito de mengano garcia"),
                                "email": openapi.Schema(type=openapi.TYPE_STRING, example="correo@test.com"),
                                "ingreso": openapi.Schema(type=openapi.TYPE_STRING, example="23/07/2024"),
                                "acceso": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=False),
                                "permisos": openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        "perfil": openapi.Schema(type=openapi.TYPE_STRING, example="Sin_Acceso"),
                                        "descripcion": openapi.Schema(type=openapi.TYPE_STRING, example="Operador sin Acceso a la cuenta"),
                                    },
                                ),
                            },
                        ),
                    ),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se encontraron operadores.",
        ),
    },
)

create_operator_docs = swagger_auto_schema(
    operation_summary="Crear un Nuevo Operador",
    operation_description="Este endpoint permite crear un nuevo operador y asignarle un perfil dentro de la cuenta.",
    tags=["Configuración"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["nombre", "paterno", "correo", "pfisica"],
        properties={
            "nombre": openapi.Schema(type=openapi.TYPE_STRING, description="Nombre del operador.", example="Pedro Gómez"),
            "paterno": openapi.Schema(type=openapi.TYPE_STRING, description="Apellido paterno del operador.", example="Gómez"),
            "materno": openapi.Schema(type=openapi.TYPE_STRING, description="Apellido materno del operador.", example="Martínez"),
            "correo": openapi.Schema(type=openapi.TYPE_STRING, description="Correo electrónico del operador.", example="pedro.gomez@example.com"),
            "pfisica": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Indica si el operador es una persona física.", example=True),
        },
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Operador creado exitosamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "idoperador": openapi.Schema(type=openapi.TYPE_INTEGER, example=2),
                    "kasociado": openapi.Schema(type=openapi.TYPE_INTEGER, example=124),
                    "nombre": openapi.Schema(type=openapi.TYPE_STRING, example="Pedro Gómez"),
                    "email": openapi.Schema(type=openapi.TYPE_STRING, example="pedro.gomez@example.com"),
                    "ingreso": openapi.Schema(type=openapi.TYPE_STRING, example="2024-10-01"),
                    "acceso": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                    "permisos": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "perfil": openapi.Schema(type=openapi.TYPE_STRING, example="dypfe_analista"),
                            "descripcion": openapi.Schema(type=openapi.TYPE_STRING, example="Analista de datos"),
                        },
                    ),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se pudo crear el operador.",
        ),
    },
)

update_operator_access_docs = swagger_auto_schema(
    operation_summary="Asignar o Revocar Acceso a un Operador",
    operation_description="Este endpoint permite asignar o revocar el acceso de un operador a la cuenta.",
    tags=["Configuración"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["idoperador"],
        properties={
            "idoperador": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID del operador.", example=2),
        },
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Acceso del operador actualizado exitosamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "idoperador": openapi.Schema(type=openapi.TYPE_INTEGER, example=2),
                    "kasociado": openapi.Schema(type=openapi.TYPE_INTEGER, example=124),
                    "nombre": openapi.Schema(type=openapi.TYPE_STRING, example="Pedro Gómez"),
                    "email": openapi.Schema(type=openapi.TYPE_STRING, example="pedro.gomez@example.com"),
                    "ingreso": openapi.Schema(type=openapi.TYPE_STRING, example="2024-10-01"),
                    "acceso": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                    "permisos": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "perfil": openapi.Schema(type=openapi.TYPE_STRING, example="dypfe_admin"),
                            "descripcion": openapi.Schema(type=openapi.TYPE_STRING, example="Administrador del sistema"),
                        },
                    ),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se pudo actualizar el acceso del operador.",
        ),
    },
)

assign_revoke_operator_role_docs = swagger_auto_schema(
    operation_summary="Asignar o Revocar Roles a un Operador",
    operation_description="Este endpoint permite asignar o revocar roles a un operador específico.",
    tags=["Configuración"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["idoperador", "perfil", "tipo_acceso"],
        properties={
            "idoperador": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID del operador.", example=2),
            "perfil": openapi.Schema(type=openapi.TYPE_STRING, description="Rol que se asignará o revocará.", example="dypfe_admin"),
            "tipo_acceso": openapi.Schema(type=openapi.TYPE_STRING, description="Acción a realizar (asignar o revocar).", example="asignar"),
        },
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Rol asignado o revocado exitosamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "idoperador": openapi.Schema(type=openapi.TYPE_INTEGER, example=2),
                    "kasociado": openapi.Schema(type=openapi.TYPE_INTEGER, example=124),
                    "nombre": openapi.Schema(type=openapi.TYPE_STRING, example="Pedro Gómez"),
                    "email": openapi.Schema(type=openapi.TYPE_STRING, example="pedro.gomez@example.com"),
                    "acceso": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                    "permisos": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "perfil": openapi.Schema(type=openapi.TYPE_STRING, example="dypfe_admin"),
                            "descripcion": openapi.Schema(type=openapi.TYPE_STRING, example="Administrador del sistema"),
                        },
                    ),
                },
            ),
        ),
        status.HTTP_403_FORBIDDEN: openapi.Response(
            description="Operador no encontrado.",
        ),
    },
)

list_available_roles_docs = swagger_auto_schema(
    operation_summary="Listar Roles Disponibles",
    operation_description="Este endpoint lista los roles disponibles para ser asignados a los operadores.",
    tags=["Configuración"],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Listado de roles exitoso.",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "rol_name": openapi.Schema(type=openapi.TYPE_STRING, example="dypfe_admin"),
                    },
                ),
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se encontraron roles.",
        ),
    },
)
