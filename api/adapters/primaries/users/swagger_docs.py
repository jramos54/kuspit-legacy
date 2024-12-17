from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi

profile_detail_docs = swagger_auto_schema(
    operation_summary="Obtener Detalle del Perfil",
    operation_description=(
        "Este endpoint permite obtener la información del perfil del usuario autenticado, incluyendo "
        "sus roles y permisos asignados."
    ),
    tags=["Dashboard"],

    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Detalle del perfil obtenido exitosamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "profile_info": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "id": openapi.Schema(
                                type=openapi.TYPE_INTEGER, description="ID único del usuario.", example=1
                            ),
                            "username": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Nombre de usuario del usuario autenticado.",
                                example="johndoe",
                            ),
                            "email": openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Correo electrónico del usuario autenticado.",
                                example="johndoe@example.com",
                            ),
                        },
                    ),
                    "roles": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        description="Lista de roles asignados al usuario, cada uno con sus permisos asociados.",
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(
                                    type=openapi.TYPE_INTEGER, description="ID único del rol.", example=10
                                ),
                                "name": openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                    description="Nombre del rol.",
                                    example="Administrador",
                                ),
                                "permissions": openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    description="Lista de permisos asociados al rol.",
                                    items=openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            "id": openapi.Schema(
                                                type=openapi.TYPE_INTEGER, description="ID único del permiso.", example=5
                                            ),
                                            "name": openapi.Schema(
                                                type=openapi.TYPE_STRING,
                                                description="Nombre del permiso.",
                                                example="can_add_user",
                                            ),
                                        },
                                    ),
                                ),
                            },
                        ),
                    ),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se encontró información del perfil.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING, example="Perfil no encontrado."),
                },
            ),
        ),
    },
)

create_user_docs = swagger_auto_schema(
    operation_summary="Crear Usuario",
    operation_description=(
        "Este endpoint permite crear un nuevo usuario en la plataforma, validando las reglas de complejidad de contraseña "
        "y asegurando que el correo electrónico y otros datos cumplen con los estándares definidos."
    ),
    tags=["Usuarios"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["correo", "password", "nombre", "paterno", "materno", "persona_fisica"],
        properties={
            "correo": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Correo electrónico del usuario.",
                example="user@example.com",
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING,
                description=(
                    "Contraseña del usuario. Debe cumplir con los siguientes requisitos:\n"
                    "- Longitud mínima de 8 caracteres.\n"
                    "- Incluir al menos una letra mayúscula, una letra minúscula, un número y un carácter especial.\n"
                    "- No contener palabras restringidas como 'deposito' ni partes del correo electrónico del usuario."
                ),
                example="SecurePass123!",
            ),
            "nombre": openapi.Schema(
                type=openapi.TYPE_STRING, description="Nombre del usuario.", example="Pedro"
            ),
            "paterno": openapi.Schema(
                type=openapi.TYPE_STRING, description="Apellido paterno del usuario.", example="López"
            ),
            "materno": openapi.Schema(
                type=openapi.TYPE_STRING, description="Apellido materno del usuario.", example="Ramírez"
            ),
            "persona_fisica": openapi.Schema(
                type=openapi.TYPE_BOOLEAN,
                description="Indica si el usuario es persona física (true) o moral (false).",
                example=True,
            ),
        },
    ),
    responses={
        status.HTTP_201_CREATED: openapi.Response(
            description="Usuario creado exitosamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(
                        type=openapi.TYPE_INTEGER, description="ID único del usuario creado.", example=1
                    ),
                    "correo": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Correo electrónico del usuario creado.",
                        example="user@example.com",
                    ),
                    "username": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Nombre de usuario generado para el usuario.",
                        example="Pedro López Ramírez",
                    ),
                    "persona_fisica": openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description="Indica si el usuario es persona física.",
                        example=True,
                    ),
                },
            ),
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description="Error al validar o crear el usuario.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING, example="El correo ya está registrado."),
                },
            ),
        ),
    },
)


