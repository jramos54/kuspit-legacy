# Librerías de Terceros
from django.urls import path

# Proyecto
from .customers_persona_fisica_views import CustomersPersonaFisicaViewSet
from .customers_persona_moral_views import CustomerPersonaMoralViewSet
from .mockapi_openfin_fisica_views import OpenFinPersonaFisicaViewSet
from .mockapi_openfin_moral_views import OpenFinPersonaMoralViewSet
from .customers_views import CustomersViewSet

# Mock Apis fisica
openfin_list_persona_fisica = {"get": "openfin_list_customer_pf"}
openfin_create_persona_fisica = {"post": "openfin_create_customer_pf"}
openfin_update_persona_fisica = {"put": "openfin_update_customer_pf"}
openfin_delete_persona_fisica = {"delete": "openfin_delete_customer_pf"}
# Mock Apis moral
openfin_list_persona_moral = {"get": "openfin_list_customer_pm"}
openfin_create_persona_moral = {"post": "openfin_create_customer_pm"}
openfin_update_persona_moral = {"put": "openfin_update_customer_pm"}
openfin_delete_persona_moral = {"delete": "openfin_delete_customer_pm"}
# persona fisica
create_customer_persona_fisica = {"post": "create_customer_persona_fisica"}
update_customer_persona_fisica = {"put": "update_customer_persona_fisica"}
delete_customer_persona_fisica = {"delete": "delete_customer_persona_fisica"}
# persona moral
create_customer_persona_moral = {"post": "create_customer_persona_moral"}
update_customer_persona_moral = {"put": "update_customer_persona_moral"}
delete_customer_persona_moral = {"delete": "delete_customer_persona_moral"}
# customers
list_customers = {"get": "list_customers"}


urlpatterns = [
    path(
        "customers",
        CustomersViewSet.as_view(
            {
                **list_customers,
            }
        ),
        name="list-customers",
    ),
    path(
        "users/onboarding/persona_fisica",
        CustomersPersonaFisicaViewSet.as_view(
            {
                **create_customer_persona_fisica,
                **update_customer_persona_fisica,
                **delete_customer_persona_fisica,
            }
        ),
        name="crud-customers-persona-fisica",
    ),
    path(
        "users/onboarding/persona_moral",
        CustomerPersonaMoralViewSet.as_view(
            {
                **create_customer_persona_moral,
                **update_customer_persona_moral,
                **delete_customer_persona_moral,
            }
        ),
        name="crud-customers-persona-moral",
    ),
    path(
        "openfin/customers_pf",
        OpenFinPersonaFisicaViewSet.as_view(
            {
                **openfin_list_persona_fisica,
                **openfin_create_persona_fisica,
                **openfin_update_persona_fisica,
                **openfin_delete_persona_fisica,
            }
        ),
        name="open-fin-mockapi-customer-fisica",
    ),
    path(
        "openfin/customers_pm",
        OpenFinPersonaMoralViewSet.as_view(
            {
                **openfin_list_persona_moral,
                **openfin_create_persona_moral,
                **openfin_update_persona_moral,
                **openfin_delete_persona_moral,
            }
        ),
        name="open-fin-mockapi-customer-moral",
    ),
]
