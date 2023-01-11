"""Test for accounts API"""
from compartidos.base_tst_class import BaseAPITest

# Librerías de Terceros
from rest_framework import status
from django.urls import reverse

ID_CONTRACT = 2
ID_PRODUCT = 2001


class AccountsAPITest(BaseAPITest):
    """API for testing account's service"""

    fixtures = [
        "fixtures/data.json",
    ]

    def test_account_opening(self):
        """function for test account opening"""
        url = reverse("accounts")
        data = {"id_producto": 2004, "nombre_wallet": "Test de wallet"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_accounts(self):
        """function for test list accounts"""
        url = reverse("accounts")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_account(self):
        """function for test detail account"""
        url = "%s?id_contract=%s" % (
            reverse("accounts"),
            ID_CONTRACT,
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_products(self):
        """function for test list products"""
        url = reverse("products")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_product(self):
        """function for test detail product"""
        url = "%s?id_product=%s" % (
            reverse("products"),
            ID_PRODUCT,
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
