from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi

create_new_password_docs = swagger_auto_schema(
    operation_summary="Creación de Nueva Contraseña",
    operation_description=(
        "Este servicio permite la creación de una nueva contraseña para el usuario."
    ),
    tags=["Seguridad"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["email"],
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING, description="Correo electrónico del usuario.", example="user@example.com"),
        },
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="La contraseña ha sido actualizada exitosamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "link": openapi.Schema(type=openapi.TYPE_STRING, example="https://example.com/reset-password"),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="El correo no fue encontrado.",
        ),
    },
)

get_security_questions_docs = swagger_auto_schema(
    operation_summary="Obtención de Preguntas de Seguridad",
    operation_description=(
        "Este servicio permite obtener las preguntas de seguridad asociadas a la cuenta del usuario para proceder con la recuperación de la contraseña."
    ),
    tags=["Seguridad"],
    manual_parameters=[
        openapi.Parameter("limit", openapi.IN_QUERY, description="Número de resultados a devolver por página (paginación).", type=openapi.TYPE_INTEGER),
        openapi.Parameter("offset", openapi.IN_QUERY, description="Índice inicial desde el cual se devuelven los resultados (paginación).", type=openapi.TYPE_INTEGER),
    ],
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Preguntas obtenidas exitosamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "link": openapi.Schema(type=openapi.TYPE_STRING, example="https://example.com/security-questions"),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se encontraron preguntas de seguridad.",
        ),
    },
)

submit_security_answers_docs = swagger_auto_schema(
    operation_summary="Envío de Respuestas a Preguntas de Seguridad",
    operation_description=(
        "Este servicio permite enviar las respuestas a las preguntas de seguridad para continuar con la recuperación de la contraseña."
    ),
    tags=["Seguridad"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["email"],
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING, description="Correo electrónico del usuario.", example="user@example.com"),
        },
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Respuestas enviadas exitosamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "link": openapi.Schema(type=openapi.TYPE_STRING, example="https://example.com/answers-submitted"),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se pudieron enviar las respuestas.",
        ),
    },
)

generate_temp_token_docs = swagger_auto_schema(
    operation_summary="Generación de Token Temporal",
    operation_description=(
        "Este servicio permite generar un token temporal para la recuperación de la contraseña."
    ),
    tags=["Seguridad"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["email"],
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING, description="Correo electrónico del usuario.", example="user@example.com"),
        },
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Token temporal generado exitosamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "link": openapi.Schema(type=openapi.TYPE_STRING, example="https://example.com/temp-token"),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se pudo generar el token temporal.",
        ),
    },
)

validate_temp_code_docs = swagger_auto_schema(
    operation_summary="Validación de Código Temporal",
    operation_description=(
        "Este servicio permite validar el código temporal generado para la recuperación de la contraseña."
    ),
    tags=["Seguridad"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["email"],
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING, description="Correo electrónico del usuario.", example="user@example.com"),
        },
    ),
    responses={
        status.HTTP_200_OK: openapi.Response(
            description="Código temporal validado exitosamente.",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "link": openapi.Schema(type=openapi.TYPE_STRING, example="https://example.com/code-validated"),
                },
            ),
        ),
        status.HTTP_404_NOT_FOUND: openapi.Response(
            description="No se pudo validar el código temporal.",
        ),
    },
)
