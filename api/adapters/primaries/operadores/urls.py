# Librerías de Terceros
from django.urls import path

# Proyecto
from .operators_views import OperatorsViewSet

create_operator = {"post": "create_operator"}
assign_roles = {"put": "assign_roles"}
grant_access={'patch':'grant_access'}
show_operator = {"get": "show_operator"} # get_operator and list_operator
list_roles = {"get":"list_roles"}

urlpatterns = [
    path(
        "operators",
        OperatorsViewSet.as_view(
            {
                **create_operator,
                **show_operator,
                **grant_access,
            }
        ),
        name="operators",
    ),
    path(
        "operators/role",
        OperatorsViewSet.as_view(
            {
                **assign_roles,
            }
        ),
        name="open-fin-mockapi-recipient",
    ),
    path(
        "operators/roles",
        OperatorsViewSet.as_view(
            {
                **list_roles,
            }
        ),
        name="operators",
    ),
]
