from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi

list_frequent_questions_docs = swagger_auto_schema(
    operation_summary="Listar Preguntas Frecuentes",
    operation_description="Este endpoint lista todas las preguntas frecuentes activas en la plataforma.",
    tags=["Ayuda"],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Listado de preguntas frecuentes exitoso.",
            schema=openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
                        "question": openapi.Schema(type=openapi.TYPE_STRING, example="¿Cómo recupero mi contraseña?"),
                        "answer": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            example="Puedes recuperar tu contraseña a través del enlace 'Olvidé mi contraseña' en la página de inicio de sesión.",
                        ),
                        "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                    },
                ),
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se encontraron preguntas frecuentes.",
        ),
    },
)

create_frequent_question_docs = swagger_auto_schema(
    operation_summary="Crear una Nueva Pregunta Frecuente",
    operation_description="Este endpoint permite crear una nueva pregunta frecuente y agregarla a la base de datos de preguntas.",
    tags=["Ayuda"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["id", "question", "answer", "is_active"],
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Identificador único de la pregunta.", example=2),
            "question": openapi.Schema(type=openapi.TYPE_STRING, description="Pregunta frecuente.", example="¿Cómo cambio mi correo electrónico?"),
            "answer": openapi.Schema(
                type=openapi.TYPE_STRING,
                description="Respuesta a la pregunta frecuente.",
                example="Para cambiar tu correo electrónico, ve a la sección 'Mi perfil' en el menú de usuario.",
            ),
            "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Indica si la pregunta está activa.", example=True),
        },
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="La pregunta frecuente se ha creado exitosamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=2),
                    "question": openapi.Schema(type=openapi.TYPE_STRING, example="¿Cómo cambio mi correo electrónico?"),
                    "answer": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Para cambiar tu correo electrónico, ve a la sección 'Mi perfil' en el menú de usuario.",
                    ),
                    "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se pudo crear la pregunta.",
        ),
    },
)

update_frequent_question_docs = swagger_auto_schema(
    operation_summary="Actualizar una Pregunta Frecuente",
    operation_description="Este endpoint permite actualizar el contenido de una pregunta frecuente existente.",
    tags=["Ayuda"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["id", "is_active"],
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Identificador único de la pregunta.", example=2),
            "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Nuevo estado de la pregunta frecuente.", example=True),
        },
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="La pregunta frecuente se ha actualizado exitosamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=2),
                    "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se pudo actualizar la pregunta.",
        ),
    },
)

