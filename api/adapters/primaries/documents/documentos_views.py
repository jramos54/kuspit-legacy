# Local utilities
from compartidos.serializers import NotFoundSerializer

# database imports
from apps.backoffice.models import users as users_models

# Librerías de Terceros
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import viewsets, parsers, status

# Django REST Framework
from drf_yasg.utils import swagger_auto_schema

# Proyecto
from . import documentos_serializer

# Libraries for upload files


class FileUploadViewSet(viewsets.GenericViewSet):
    """class for file CRUD view"""

    permission_classes = [DjangoModelPermissions]
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)
    queryset = users_models.User.objects.all()

    @swagger_auto_schema(
        request_body=documentos_serializer.DataDocumentSerializer(),
        responses={
            status.HTTP_200_OK: documentos_serializer.DocumentSerializer(many=True),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def upload_documents(self, request, doc_type, *args, **kwargs) -> Response:
        """function for upload one or more files"""

        files = request.FILES
        for file in files:
            print(type(file))
        print(doc_type)

        return Response({}, status=status.HTTP_201_CREATED)
