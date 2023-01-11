"""Test for frequent questions API"""
from compartidos.base_tst_class import BaseAPITest

# Librerías de Terceros
from rest_framework import status
from django.urls import reverse

QUESTION_ID = 1


class FrequentQuestionsAPITest(BaseAPITest):
    """API for testing Frequent Questions CRUD"""

    fixtures = [
        "fixtures/data.json",
    ]

    def test_list_questions(self):
        """function for test list customes"""
        url = reverse("list-frequent-questions")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_question(self):
        """function for test detail question"""
        url = "%s?question_id=%s" % (reverse("list-frequent-questions"), QUESTION_ID)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_question(self):
        """function for test create question"""
        url = reverse("crud-frequent-questions")
        data = {
            "answer": "¿Qué es DyP?",
            "question": "Somos una institución de fondos de pago electrónico (IFPE) mexicana que le brinda a sus clientes una plataforma de pagos electrónicos para recibir y efectuar depósitos vía el SPEI con la finalidad de eficientar los procesos de tesorería de empresas y personas con actividad empresarial y profesional.",
            "is_active": "True",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_frequent_question(self):
        """fuction for tests update frequent question"""
        url = "%s?question_id=%s" % (reverse("crud-frequent-questions"), QUESTION_ID)
        data = {
            "answer": "¿Qué es DyP?",
            "question": "Somos una institución de fondos de pago electrónico (IFPE) mexicana que le brinda a sus clientes una plataforma de pagos electrónicos para recibir y efectuar depósitos vía el SPEI con la finalidad de eficientar los procesos de tesorería de empresas y personas con actividad empresarial y profesional.",
            "is_active": "False",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
