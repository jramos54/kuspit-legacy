"""Test for products API"""
from compartidos.base_tst_class import BaseAPITest

# Librerías de Terceros
from rest_framework import status
from django.urls import reverse

ID_PRODUCT = 2001


class AccountsAPITest(BaseAPITest):
    """API for testing account's service"""

    fixtures = [
        "fixtures/data.json",
    ]

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
