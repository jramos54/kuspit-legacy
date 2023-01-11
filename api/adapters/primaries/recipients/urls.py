# Librerías de Terceros
from django.urls import path

# Proyecto
from .mockapi_openfin_recipients_views import OpenFinRecipientsViewSet
from .recipients_views import RecipientsViewSet

create_recipient = {"post": "create_recipient"}
update_recipient = {"put": "update_recipient"}
delete_recipient = {"delete": "delete_recipient"}
list_recipients = {"get": "list_recipients"}

urlpatterns = [
    path(
        "recipient",
        RecipientsViewSet.as_view(
            {
                **create_recipient,
                **update_recipient,
                **delete_recipient,
                **list_recipients,
            }
        ),
        name="recipients",
    ),
]
