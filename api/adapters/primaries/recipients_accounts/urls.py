# Librerías de Terceros
from django.urls import path

# Proyecto
from .recipients_accounts_views import RecipientsAccountViewSet

create_recipient_account = {"post": "create_recipient_account"}
update_recipient_account = {"put": "update_recipient_account"}
delete_recipient_account = {"delete": "delete_recipient_account"}


urlpatterns = [
    path(
        "recipient_account",
        RecipientsAccountViewSet.as_view(
            {
                **create_recipient_account,
                **update_recipient_account,
                **delete_recipient_account,
            }
        ),
        name="recipients_accounts",
    ),
]
