from django.urls import path
from .customers_views import CustomersViewSet

list_customers = {"get": "list_customers"}
create_customer = {"post": "create_customer"}
update_customer = {"put": "update_customer"}
delete_customer = {"delete": "delete_customer"}

urlpatterns = [
    path(
        "customers", CustomersViewSet.as_view({**list_customers,
                                               **create_customer,
                                               **update_customer,
                                               **delete_customer
                                               }
                                              ),
        name="crud-customers"
    ),
]
