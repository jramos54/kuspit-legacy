from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from apps.backoffice.models.administrators import Administrator

CUSTOMER_ID = 1


class CustomersAPITest(TestCase):
    """API for testing customer's CRUD"""

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

        self.email = "dj-superadmin@paycode.io"
        self.password = "admin123"
        self.user = Administrator.objects.get(email=self.email)
        self.api_authentication(self.user.email, self.password)

    def api_authentication(self, email: str, password: str):
        credentials = self.get_credentials(email, password)
        token = credentials.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_list_payments(self):
        url = reverse("payments")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
