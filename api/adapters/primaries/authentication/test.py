# Librerias Estandar

# Variables de Configuración
from configuracion.settings import URL_BASE_OPENFIN

from apps.backoffice.models import User

# Librerías de Terceros
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.test import TestCase
from requests import request


class LoginAPITest(TestCase):
    """API for testing login"""

    fixtures = [
        "fixtures/data.json",
    ]

    def setUp(self) -> None:
        self.client = APIClient()

    def test_login(self):
        url = reverse("token_obtain")
        data = {
            "email": "dj-superadmin@forte.io",
            "password": "admin123",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_openfin(self):
        url = f"http://{URL_BASE_OPENFIN}/rpc/auth"
        payload = "username=demo%40sinc.com.mx&pass=DemoSINC01"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = request("POST", url, headers=headers, data=payload)
        print(response.text)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unit_token_vs_openfin_token(self):
        url = URL_BASE_OPENFIN + "/rpc/auth"
        data = {
            "username": "demo@sinc.com.mx",
            "password": "DemoSINC01",
        }
        response = self.client.post(url, data, format="json")
        token_openfin = response.data["access"]
        user_id = User.objects.filter(email=data["username"]).first().id
        token_unit = OutstandingToken.objects.filter(user_id=user_id).first().token
        self.assertEqual(token_openfin, token_unit)
