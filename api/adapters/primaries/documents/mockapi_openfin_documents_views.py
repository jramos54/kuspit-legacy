"""mockapi for customer persona moral"""
from compartidos.serializers import NotFoundSerializer

# database imports
from apps.backoffice.models import users as users_models

# Librerías de Terceros
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema

# Proyecto
from . import documentos_serializer

document_type = {"idtipo": 1, "nombre": "foto"}

document = {
    "id": 1,
    "idtipo": 1,
    "b64": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAMDAwMDAwQEBAQFBQUFB",
}

DOCUMENT_TYPE_LIST_DATA = [
    document_type,
]
DOCUMENTS_LIST = [
    document,
]


class OpenFinDocumentsViewSet(viewsets.GenericViewSet):
    # permission_classes = [DjangoModelPermissions]
    queryset = users_models.User.objects.all()
    parser_classes = (JSONParser,)
    serializer_class = documentos_serializer.OpenFinDocumentsSerializer
    """
    MockApi de OpenFin para documentos
    """

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: documentos_serializer.OpenFinCatDocumentsSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def openfin_list_cat_documents(self, request) -> Response:
        """
        function to get all type documents
        """
        query_params = request.query_params
        query_params.get("id", None)
        list_data = DOCUMENT_TYPE_LIST_DATA
        data_serialized = documentos_serializer.OpenFinCatDocumentsSerializer(
            data=list_data, many=True
        )
        data_serialized.is_valid(raise_exception=True)

        return Response(data_serialized.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            status.HTTP_201_CREATED: documentos_serializer.OpenFinDocumentsSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def openfin_upload_document(self, request) -> Response:
        """
        function to assign document to user
        """
        data = request.data
        data["id"] = request.user.id
        data_serialized = documentos_serializer.OpenFinDocumentsSerializer(data=data)
        data_serialized.is_valid(raise_exception=True)

        DOCUMENTS_LIST.append(data)

        return Response(data_serialized.data, status=status.HTTP_201_CREATED)
