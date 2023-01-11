from compartidos.base_tst_class import BaseAPITest

# Librerías de Terceros
from rest_framework import status
from django.urls import reverse


class MovementsByMonthAPITest(BaseAPITest):
    """API for testing payment's CRUD"""

    fixtures = [
        "fixtures/data.json",
    ]

    def test_list_movements_by_month(self):
        """Function to test the list movements by account"""
        kauxiliar = 5

        url = f"{reverse('movements-historical')}?kauxiliar={kauxiliar}"
        response = self.client.get(url)
        self._logout()
        print(f"respuesta de tests {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
