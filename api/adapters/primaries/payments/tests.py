from compartidos.base_tst_class import BaseAPITest

# Librerías de Terceros
from rest_framework import status
from django.urls import reverse

ID_PAGO = 1


class CustomersAPITest(BaseAPITest):
    """API for testing payment's CRUD"""

    fixtures = [
        "fixtures/data.json",
    ]

    def test_new_payment_schedule(self):
        """Test for create a new payment"""
        url = reverse("payments")
        data = {
            "kauxiliar": 1,
            "iddestinatario": 1,
            "idcuenta": 1,
            "monto": 6930.18,
            "descripcion": "Deserunt eligendi quam voluptatum",
            "fechapago": "07/12/2004",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_payments(self):
        """function for test list payments"""
        url = reverse("payments")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
