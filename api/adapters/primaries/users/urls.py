# Librerías de Terceros
from django.urls import path

# Proyecto
from .users_views import PermissionsViewSet

profile_detail = {"get": "profile_detail"}
create_user = {"post": "create_user"}

urlpatterns = [
    path(
        "users/profile",
        PermissionsViewSet.as_view(
            {
                **profile_detail,
            }
        ),
        name="profile",
    ),
    path(
        "users/create_user",
        PermissionsViewSet.as_view(
            {
                **create_user,
            }
        ),
        name="create-user",
    ),
]
