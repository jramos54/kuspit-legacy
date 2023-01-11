# Librerías de Terceros
from django.urls import path

# Proyecto
from .recovery_password_views import RecoveryPasswordViewSet

generate_token = {"post": "generate_token"}
get_questions = {"get": "get_questions"}
send_answers = {"post": "send_answers"}
new_password = {"post": "new_password"}
validate_code = {"post": "validate_code"}


urlpatterns = [
    path(
        "recovery/temp-token",
        RecoveryPasswordViewSet.as_view(
            {
                **generate_token,
            }
        ),
        name="temp-token",
    ),
    path(
        "recovery/preguntas",
        RecoveryPasswordViewSet.as_view(
            {
                **get_questions,
                **send_answers
            }
        ),
        name="preguntas",

    ),
    path(
        "recovery/new-password",
        RecoveryPasswordViewSet.as_view(
            {
                **new_password,
            }
        ),
        name="new-password",
    ),
    path(
            "recovery/validate-code",
            RecoveryPasswordViewSet.as_view(
                {
                    **validate_code,
                }
            ),
            name="validate-code",
        ),
]
