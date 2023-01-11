from compartidos.base_tst_class import BaseAPITest

# Librerías de Terceros
from rest_framework import status
from django.urls import reverse

CUSTOMER_ID = 1


class BeneficiaryAPITest(BaseAPITest):
    """API for testing customer's CRUD"""

    fixtures = [
        "fixtures/data.json",
    ]

    def test_list_beneficiario(self):
        """function for test list Beneficiary"""
        url = reverse("beneficiarios")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_beneficiario(self):
        """function for test create recipients"""
        url = reverse("beneficiarios")

        data = {
            "nombre": "Arioto",
            "paterno": "Ramos",
            "materno": "Molina",
            "fecha_nacimiento": "2016-11-02",
            "calle": "av evergreen",
            "numext": "3",
            "numint": "0",
            "pais": "Mexico",
            "estado": "estado de Mexico",
            "ciudad": "zumpango",
            "alcaldia": "Zumpango",
            "cp": "55620",
            "parentesco": "perro",
            "porcentaje": 0.99,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_beneficiario(self):
        """function for test update beneficiario"""
        url = "%s?user_id=%s" % (reverse("beneficiarios"), CUSTOMER_ID)
        data = {
            "openfin_id": 1,
            "idasociado": 1,
            "openfin_info": {
                "nombre": "Arioto",
                "paterno": "Ramos",
                "materno": "Molina",
                "fecha_nacimiento": "2016-11-02",
                "calle": "av evergreen",
                "numext": "3",
                "numint": "0",
                "pais": "Mexico",
                "estado": "estado de Mexico",
                "ciudad": "zumpango",
                "alcaldia": "Zumpango",
                "cp": "55620",
                "parentesco": "perro",
                "porcentaje": 0.5,
            },
        }
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_beneficiario(self):
        """function for test delete beneficiary"""
        url = "%s?user_id=%s" % (reverse("beneficiarios"), CUSTOMER_ID)
        data = {
            "user_id": 1,
            "openfin_info": {
                "nombre": "Arioto",
                "paterno": "Ramos",
                "materno": "Molina",
                "fecha_nacimiento": "2016-11-02",
                "calle": "av evergreen",
                "numext": "3",
                "numint": "0",
                "pais": "Mexico",
                "estado": "estado de Mexico",
                "ciudad": "zumpango",
                "alcaldia": "Zumpango",
                "cp": "55620",
                "parentesco": "perro",
                "porcentaje": 0.99,
            },
        }
        response = self.client.delete(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
