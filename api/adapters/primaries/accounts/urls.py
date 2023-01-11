"""accounts urls"""
# Librerías de Terceros
from django.urls import path

# Proyecto
from .accounts_views import AccountsViewSet

# openning account
create_account = {"post": "create_account"}
list_accounts = {"get": "list_accounts"}


urlpatterns = [
    path(
        "accounts",
        AccountsViewSet.as_view(
            {
                **create_account,
                **list_accounts,
            }
        ),
        name="accounts",
    ),
]
