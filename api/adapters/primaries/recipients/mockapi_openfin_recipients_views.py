from compartidos.serializers import NotFoundSerializer

# Librerías de Terceros
from rest_framework.response import Response
from rest_framework import viewsets, status

# Django REST Framework
from drf_yasg.utils import swagger_auto_schema

# Proyecto
from . import recipients_serializer

recipient_dummy = {
    "openfin_id": 1,
    "idasociado": 1,
    "nombre_completo": "Joel Ramos Molina",
    "alias": "Yoil",
    "institucion_bancaria": "BBVA",
    "cuenta": 1234567890,
    "catalogo_cuenta": "value4",
    "limite_de_operaciones": 200,
    "rfc": "RAMJ850504IN3",
    "curp": "RAMJ850504HMCMLL02",
    "is_active": True,
}
LIST_DATA = [
    recipient_dummy,
]


class OpenFinRecipientsViewSet(viewsets.GenericViewSet):
    """Views for CRUD Recipients"""

    serializer_class = recipients_serializer.RecipientSerializer

    @swagger_auto_schema(
        request_body=recipients_serializer.RecipientSerializer(),
        responses={
            status.HTTP_200_OK: recipients_serializer.RecipientSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def create_destinatario(self, request) -> Response:
        """dar de alta un destinatario"""
        data = request.data
        data_serialized = recipients_serializer.RecipientSerializer(data=data)
        data_serialized.is_valid(raise_exception=True)
        list_data = LIST_DATA

        list_data.append(data_serialized.validated_data)

        serializer = recipients_serializer.RecipientSerializer(
            data=data_serialized.validated_data
        )
        serializer.is_valid(raise_exception=True)

        message = """
        El destinatario fue dado de alta exitosamente,
        puedes realizarle transferencias después de los 30 minutos.
        """
        response_data = {
            "message": message,
            "data": serializer.data,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
