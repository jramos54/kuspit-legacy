# Librerías de Terceros
from django.urls import path

# Proyecto
from .movements_historical_views import MovementsByMonthViewSet

list_movements = {"get": "list_movements_by_month"}

urlpatterns = [
    path(
        "movements-historical",
        MovementsByMonthViewSet.as_view(
            {
                **list_movements,
            }
        ),
        name="movements-historical",
    )
]
