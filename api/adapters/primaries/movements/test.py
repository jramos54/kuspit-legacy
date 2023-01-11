from compartidos.base_tst_class import BaseAPITest

# Librerías de Terceros
from rest_framework import status
from django.urls import reverse


class CustomersAPITest(BaseAPITest):
    """API for testing payment's CRUD"""

    fixtures = [
        "fixtures/data.json",
    ]

    def test_list_movements_by_account(self):
        """Function to test the list movements by account"""
        kauxiliar = 5
        defecha = "2023-01-01"
        afecha = "2023-12-31"
        limite = 0

        url = f"{reverse('movements')}?kauxiliar={kauxiliar}&defecha={defecha}&afecha={afecha}&limite={limite}"
        response = self.client.get(url)
        self._logout()
        print(f"respuesta de tests {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
