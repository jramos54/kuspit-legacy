from django.contrib.gis.geos import Point
from django.test import TestCase
from django.urls import reverse
from apps.backoffice.models.users import User
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework import status
from rest_framework.test import APIClient


class BaseAPITest(TestCase):
    """API for testing user authenticated services"""

    fixtures = [
        "fixtures/data.json",
    ]

    def get_credentials(self, email, password):
        url = reverse("token_obtain")
        response = self.client.post(url, {
            'email': email,
            'password': password
        })
        return response.data

    def setUp(self) -> None:
        self.client = APIClient()
        self.email = "demo@sinc.com.mx"
        self.password = "DemoSINC01"
        self.api_authentication(self.email, self.password)

    def api_authentication(self, email: str, password: str):
        credentials = self.get_credentials(email, password)
        self.token = credentials.get('access')
        self.refresh_token = credentials.get('refresh')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.user = User.objects.get(email=self.email)

    def _logout(self):
        url = reverse("logout")
        data = {"refresh": self.refresh_token}
        self.client.post(url, data, format="json")
        print('logout exitoso')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
