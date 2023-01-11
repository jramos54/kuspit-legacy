# Librerías de Terceros
from django.urls import path

# Proyecto
from .change_password_views import ChangePasswordViewSet


cambiar_password = {"post": "cambiar_password"}

urlpatterns = [
    path(
        "cambiar-password",
        ChangePasswordViewSet.as_view(
            {
                **cambiar_password,
            }
        ),
        name="cambiar-password",
    )
]
