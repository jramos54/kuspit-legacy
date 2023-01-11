"""Test for customer API"""
from compartidos.base_tst_class import BaseAPITest

# Librerías de Terceros
from rest_framework import status
from django.urls import reverse

CUSTOMER_ID = 1
OPENFIN_ID = 1
IDTIPO = 1


class FileUploadTest(BaseAPITest):
    """Class for testing carga de documentos CRUD"""

    def test_openfin_get_cat_documents(self):
        """Test for get all type documents"""
        url = reverse("openfin_list_cat_documents")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
