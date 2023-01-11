# Librerías de Terceros
from django.urls import path

# Proyecto
from .beneficiary_views import BeneficiaryViewSet

create_beneficiario = {"post": "create_beneficiario"}
update_beneficiario = {"patch": "update_beneficiario"}
delete_beneficiario = {"delete": "delete_beneficiario"}
list_beneficiario = {"get": "list_beneficiario"}

urlpatterns = [
    path(
        "beneficiario",
        BeneficiaryViewSet.as_view(
            {
                **create_beneficiario,
                **update_beneficiario,
                **delete_beneficiario,
                **list_beneficiario,
            }
        ),
        name="beneficiarios",
    )
]
