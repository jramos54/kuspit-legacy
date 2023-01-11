"""Test for recipients API"""
from compartidos.base_tst_class import BaseAPITest

# Librerías de Terceros
from rest_framework import status
from django.urls import reverse

CUSTOMER_ID = 1


class RecipientsAPITest(BaseAPITest):
    """API for testing customer's CRUD"""

    fixtures = [
        "fixtures/data.json",
    ]

    def test_list_destinatario(self):
        """function for test list recipients"""
        url = reverse("recipients")
        response = self.client.get(url)
        print(response.status_code)
        self._logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_destinatario(self):
        """function for test list recipients"""
        iddestinatario = "33"
        url = f"{reverse('recipients')}?iddestinatario={iddestinatario}"
        response = self.client.get(url)
        self._logout()
        print(f"respuesta de tests {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_destinatario(self):
        """function for test create recipients"""
        url = reverse("recipients")

        data = {
            "nombre": "riegel",
            "paterno": "ramos",
            "materno": "molina",
            "alias": "mascota",
            "rfc": "RAMR200312H00",
            "curp": "RAMR200312HMCMLL00",
            "is_active": True,
            "correo": "riegel@gmail.com",
            "pfisica": True,
        }

        response = self.client.post(url, data, format="json")
        print(f"esto es del test {response.data}")
        self._logout()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_destinatario(self):
        """function for test update recipient"""

        data = {
            "iddestinatario": 20,
            "nombre": "Piyush",
            "paterno": "ramos",
            "materno": "molina",
            "alias": "Mascota",
            "rfc": "RAMP200312H00",
            "curp": "RAMP200312HMCMLL00",
            "is_active": True,
            "correo": "piyush@gmail.com",
            "pfisica": True,
        }
        url = "%s?iddestinatario=%s" % (reverse("recipients"), data["iddestinatario"])
        response = self.client.put(url, data, format="json")
        self._logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_destinatario(self):
        """function for test delete recipient"""

        data = {"iddestinatario": 20}
        url = "%s?iddestinatario=%s" % (reverse("recipients"), data["iddestinatario"])
        response = self.client.delete(url)
        self._logout()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wrong_CURP(self):
        """function for test create recipients"""
        url = reverse("recipients")

        data = {
            "nombre": "riegel",
            "paterno": "ramos",
            "materno": "molina",
            "alias": "mascota",
            "rfc": "RAMR200312H35",
            "curp": "RAMR200312HMCLL92",
            "is_active": True,
            "correo": "riegel@gmail.com",
            "pfisica": True,
        }

        response = self.client.post(url, data, format="json")
        print(f"esto es del test {response.data}")
        self._logout()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
