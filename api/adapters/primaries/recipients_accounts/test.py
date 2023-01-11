"""Test for recipients API"""
# Librerias Estandar
import json

from compartidos.base_tst_class import BaseAPITest

# Librerías de Terceros
from rest_framework import status
from django.urls import reverse

CUSTOMER_ID = 1


class RecipientsAccountAPITest(BaseAPITest):
    """API for testing customer's CRUD"""

    fixtures = [
        "fixtures/data.json",
    ]

    def test_create_recipient_account(self):
        """function for test create recipients"""
        url = reverse("recipients_accounts")

        data = {
            "iddestinatario": 45,
            "cuenta": 8000000000000001,
            "institucion_bancaria": "BBVA BANCOMER",
            "catalogo_cuenta": "TARJETA",
            "is_active": True,
            "limite_operaciones": 100,
            "limite": 25000,
        }

        response = self.client.post(url, data, format="json")
        print(f"esto es del test {response.data}")
        self._logout()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_recipient_account(self):
        """function for test update recipient"""

        data = {
            "idcuenta": 13,
            "is_active": True,
            "limite_operaciones": 1000,
            "limite": 50000,
            "alias": "test",
        }
        url = reverse("recipients_accounts")
        response = self.client.put(
            url, data=json.dumps(data), content_type="application/json"
        )  # , format="json"
        self._logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_recipient_account(self):
        """function for test delete recipient"""
        data = {"idcuenta": 215, "iddestinatario": 45}
        url = "%s?idcuenta=%siddestinatario=%s" % (
            reverse("recipients_accounts"),
            data["idcuenta"],
            data["iddestinatario"],
        )

        response = self.client.delete(url, data, format="json")
        self._logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
