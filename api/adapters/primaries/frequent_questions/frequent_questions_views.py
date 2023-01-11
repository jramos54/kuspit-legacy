"""views for frequent questions service"""
# Local utilities
from compartidos.serializers import NotFoundSerializer

# Database imports
from apps.webApp.models import frequent_questions as frequent_questions_models

# Librerías de Terceros
# Django REST Framework
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import viewsets, status

# Third party libraries
from drf_yasg.utils import swagger_auto_schema

# Proyecto
# Project, frequent questions engine imports
from ....adapters.secondaries.factory import (
    constructor_frequent_questions as frequent_questions_repo,
)
from ....engine.domain.exceptions import exceptions_frequent_questions as exceptions
from ....engine.use_cases import factory as frequent_questions_engine
from . import frequent_questions_serializers

# Frequent questions engine implementation
frequent_questions_repository = frequent_questions_repo.constructor_frequent_questions(
    frequent_questions_models.FrequentQuestions
)
frequent_questions_engine = (
    frequent_questions_engine.constructor_manager_frequent_questions(
        frequent_questions_repository
    )
)


class FrequentQuestionsViewSet(viewsets.GenericViewSet):
    """class for frequent questions views without authentication"""

    serializer_class = frequent_questions_serializers.FrequentQuestionsSerializer

    @swagger_auto_schema(
        operation_summary="Lista las preguntas frecuentes",
        operation_description="Listado de preuntas frecuentes activas",
        query_serializer=frequent_questions_serializers.FrequentQuestionsQueryParamsSerializer(),
        responses={
            status.HTTP_200_OK: frequent_questions_serializers.FrequentQuestionsSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
        tags=['Preguntas Frecuentes']

    )
    def list_frequent_questions(self, request):
        """list/Retrieve frequent questions service"""
        query_params = request.query_params
        query_serializer = (
            frequent_questions_serializers.FrequentQuestionsQueryParamsSerializer(
                data=query_params
            )
        )
        query_serializer.is_valid(raise_exception=True)
        id_question = query_serializer.validated_data.get("id")
        # Filter list by queryparams
        if id_question is not None:
            frequent_question_data = frequent_questions_engine.get_frequent_questions(
                id=id_question
            )
            get_frequent_question = (
                frequent_questions_serializers.FrequentQuestionsSerializer(
                    data=frequent_question_data.__dict__
                )
            )
            get_frequent_question.is_valid(raise_exception=True)
            frequent_question = get_frequent_question.validated_data
            response_data = {
                "detail": "",
                "data": frequent_question,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        list_data = frequent_questions_engine.list_frequent_questions()
        list_data = [entidad.__dict__ for entidad in list_data]
        list_frequenten_questions = (
            frequent_questions_serializers.FrequentQuestionsSerializer(
                data=list_data, many=True
            )
        )
        list_frequenten_questions.is_valid(raise_exception=True)
        response_data = {
            "detail": "",
            "data": list_frequenten_questions.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class FrequentQuestionsAuthViewSet(viewsets.GenericViewSet):
    """class for frequent questions views with authentication"""

    queryset = frequent_questions_models.FrequentQuestions.objects.all()
    permission_classes = [DjangoModelPermissions]
    serializer_class = frequent_questions_serializers.FrequentQuestionsSerializer

    @swagger_auto_schema(
        operation_summary="Crear una nueva pregunta",
        operation_description="Crea una nueva pregunta y se agrega a la base de preguntas",
        request_body=frequent_questions_serializers.FrequentQuestionsSerializer(),
        responses={
            status.HTTP_200_OK: frequent_questions_serializers.FrequentQuestionsSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
        tags=['Preguntas Frecuentes']

    )
    def create_frequent_questions(self, request) -> Response:
        """fuction to create one frequent question"""
        data = request.data
        frequent_question_serialized = (
            frequent_questions_serializers.FrequentQuestionsSerializer(data=data)
        )
        frequent_question_serialized.is_valid(raise_exception=True)
        request_user = request.user

        if request_user.email == "demo@sinc.com.mx":
            try:
                frequent_question = frequent_questions_engine.create_frequent_questions(
                    question=frequent_question_serialized.validated_data.get(
                        "question"
                    ),
                    answer=frequent_question_serialized.validated_data.get("answer"),
                    is_active=frequent_question_serialized.validated_data.get(
                        "is_active"
                    ),
                )
                frequent_question_dict = frequent_question.__dict__
            except exceptions.QuestionAlreadyExist:
                return Response(
                    exceptions.QuestionAlreadyExist(
                        frequent_question_serialized.validated_data.get("question")
                    ).message,
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            response_data = {
                "detail": "Permiso denegado, no cuentas con los permisos necesarios para poder utilizar este servicio",
                "data": data,
            }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        frequent_question_serializer = (
            frequent_questions_serializers.FrequentQuestionsSerializer(
                data=frequent_question_dict
            )
        )
        frequent_question_serializer.is_valid(raise_exception=True)
        response_data = {
            "detail": "",
            "data": frequent_question_serialized.data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Actualiza una pregunta frecuente",
        operation_description="Actualiza el contenido de la pregunta seleccionada",
        request_body=frequent_questions_serializers.FrequentQuestionsQueryParamsSerializer(),
        responses={
            status.HTTP_200_OK: frequent_questions_serializers.FrequentQuestionsQueryParamsSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
        tags=['Preguntas Frecuentes']

    )
    def update_frequent_questions(self, request):
        """fuction for update a frequent question"""
        query_params_serialized = (
            frequent_questions_serializers.FrequentQuestionsSerializer(
                data=request.data
            )
        )
        query_params_serialized.is_valid(raise_exception=True)
        request_user = request.user

        if request_user.email == "demo@sinc.com.mx":
            try:
                frequent_question = frequent_questions_engine.update_frequent_questions(
                    id=query_params_serialized.validated_data.get("id"),
                    question=None,
                    answer=None,
                    is_active=query_params_serialized.validated_data.get("is_active"),
                )

                frequent_question_serialized = (
                    frequent_questions_serializers.FrequentQuestionsSerializer(
                        data=frequent_question.__dict__
                    )
                )
            except exceptions.QuestionNoExist:
                return Response(
                    exceptions.QuestionNoExist(
                        frequent_question_serialized.validated_data.get("id")
                    ).message,
                    status=status.HTTP_400_BAD_REQUEST,
                )

        frequent_question_serialized.is_valid(raise_exception=True)
        response_data = {
            "detail": "",
            "data": frequent_question_serialized.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)
