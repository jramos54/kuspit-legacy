# Librerías de Terceros
from django.urls import path

# Proyecto
from .payments_views import PaymentsViewSet

# openning payment
create_payment = {"post": "create_payment"}
list_payments = {"get": "list_payments"}
delete_payment = {"delete": "delete_payment"}


urlpatterns = [
    path(
        "payments",
        PaymentsViewSet.as_view({**create_payment, **list_payments, **delete_payment}),
        name="payment",
    ),
]
