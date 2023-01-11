# Librerías de Terceros
from django.urls import path

# Proyecto
from .movements_views import MovementsViewSet

list_movements = {"get": "list_movements_by_account"}

urlpatterns = [
    path(
        "movements",
        MovementsViewSet.as_view(
            {
                **list_movements,
            }
        ),
        name="movements",
    )
]
