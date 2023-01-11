from compartidos.base_tst_class import BaseAPITest

# Librerías de Terceros
from rest_framework import status
from django.urls import reverse


class AdministratorsAPITest(BaseAPITest):
    """API for testing users services"""

    fixtures = [
        "fixtures/data.json",
    ]

    def test_profile_detail(self):
        url = reverse("profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_report_location(self):
        # Create a fake request object with predetermined values
        url = reverse("profile-location")
        payload = {"location": {"latitude": 40.7128, "longitude": -74.006}}

        response = self.client.post(url, payload, format="json")

        # TODO: unittest for response.data validation

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        url = reverse("create-user")

        # Happy path
        data = {
            "email": "maguila@nxuni.io",
            "password": "szGeRQY)D+He4g)b",
            "username": "maguila",
            "is_staff": True,
            "is_customer": False,
            "is_persona_fisica": False,
            "is_persona_moral": False,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Email in password validation
        data = {
            "email": "customer@nxuni.io",
            "password": "customer@nxuni.io",
            "username": "customer",
            "is_staff": True,
            "is_customer": False,
            "is_persona_fisica": False,
            "is_persona_moral": False,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # More than 3 identical consecutive alphanumeric password validation
        data = {
            "email": "another@nxuni.io",
            "password": "-Holaaas971",
            "username": "another_customer",
            "is_staff": True,
            "is_customer": False,
            "is_persona_fisica": False,
            "is_persona_moral": False,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PasswordResetAPITest(BaseAPITest):
    """API for testing reset password services"""

    fixtures = [
        "fixtures/data.json",
    ]

    def test_create_code(self):
        url = reverse("reset-password")
        data = {
            "email": "dj-superadmin@forte.io",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_confirm_reset_code(self):
        url = reverse("reset-code-confirm")

        data = {
            "user": {"email": "dj-superadmin@forte.io"},
            "code": 12345,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_resend_reset_code(self):
        url = reverse("resend-reset-code")
        data = {
            "email": "dj-superadmin@forte.io",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_reset_confirm(self):
        url = reverse("reset-password")
        data = {
            "email_code": {"email": "raul@gmail.com", "reset_code": "testpassword"},
            "password": "t3st@Password",
            "confirm_password": "t3st@Password",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
