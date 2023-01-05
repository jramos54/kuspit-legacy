from django.urls import path
from .payments_views import CustomersPaymentsViewSet

list_payments = {"get": "list_payments"}

urlpatterns = [
    path(
        "payments", CustomersPaymentsViewSet.as_view({**list_payments,
                                                      }
                                                     ),
        name="payments"
    ),
]
