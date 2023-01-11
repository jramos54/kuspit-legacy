"""Test for recipients API"""
from compartidos.base_tst_class import BaseAPITest

# Librerías de Terceros
from rest_framework import status
from django.urls import reverse

CUSTOMER_ID = 1


class BankAPITest(BaseAPITest):
    """API for testing customer's CRUD"""

    fixtures = [
        "fixtures/data.json",
    ]

    def test_list_banks(self):
        """function for test list recipients"""
        url = reverse("bank")
        response = self.client.get(url)
        print(f"respuesta de tests {response.status_code}")
        self._logout()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bank_detail(self):
        nombre = "BBVA"
        url = f"{reverse('bank')}?nombre={nombre}"
        print(url)
        response = self.client.get(url)
        print(f"respuesta de tests {response.status_code}")
        self._logout()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
