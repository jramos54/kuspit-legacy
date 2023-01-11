"""Views for customer persona fisica API"""

# Local utilities
from compartidos.serializers import NotFoundSerializer

# database imports
from apps.backoffice.models import users as users_models

# Librerías de Terceros
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import viewsets, status

# Django REST Framework
from drf_yasg.utils import swagger_auto_schema

# Proyecto
# engine imports
from ....adapters.secondaries.factory import (
    constructor_customers as customer_repository,
)
from ....engine.use_cases import factory as customer_engine
from . import customers_persona_fisica_serializer, customers_serializers

# customer engine implementation
customers_repository = customer_repository.constructor_customers(users_models.User)
customers_engine = customer_engine.constructor_manager_customers(customers_repository)


customer_dummy = {
    "id": 1,
    "user_id": 1,
    "openfin_info": {
        "nombre": "MARCO",
        "paterno": "AGUILA",
        "materno": "MEDRANO",
        "sexo": "SIEMPRE",
        "fechanacimiento": "2000-01-01",
        "lugarnacimiento": {
            "municipio": "Monterrey",
            "estado": "Nuevo León",
            "pais": "México",
        },
        "pais_nacionalidad": "1",
        "claveelector": "123123123ssa2233",
        "domicilio": {
            "calle": "unacalle",
            "numext": "unnumext",
            "numint": "unnumint",
            "colonia": "unacolonia",
            "cp": "uncp",
            "municipio": "unmunicipio",
            "estado": "unestado",
            "entrecalles": "algunasentrecalles",
            "pais": "nombredelpais",
        },
        "profesion": "0",
        "ocupacion": "0",
        "rfc": "1234567890123",
        "curp": "123456789012345678",
        "email": "un@email.io",
        "telefono": "8117480407",
        "idsucursal": "1",
        "idrol": "10",
        "estadocivil": "0",
    },
}
LIST_DATA = [
    customer_dummy,
]


class CustomersViewSet(viewsets.GenericViewSet):
    """
    Customer's ViewSet
    """

    permission_classes = [DjangoModelPermissions]
    queryset = users_models.User.objects.all()

    @swagger_auto_schema(
        query_serializer=customers_serializers.QueryParamsCustomerSerializer(),
        responses={
            status.HTTP_200_OK: customers_persona_fisica_serializer.CustomerPersonaFisicaSerializer(
                many=True
            ),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def list_customers(self, request) -> Response:
        """function for list and detail of customer persona fisica"""
        query_params = request.query_params
        query_params_serialized = customers_serializers.QueryParamsCustomerSerializer(
            data=query_params
        )
        query_params_serialized.is_valid(raise_exception=True)

        customers = customers_engine.list_customers(query_params_serialized.data)

        page = self.paginate_queryset(customers)
        if page is not None:
            serializer = customers_serializers.BaseCustomerSerializer(
                data=page, many=True
            )
            serializer.is_valid(raise_exception=False)
            return self.get_paginated_response(serializer.data)

        customers_serialized = customers_serializers.BaseCustomerSerializer(
            data=customers, many=True
        )
        customers_serialized.is_valid(raise_exception=False)
        return Response(customers_serialized.data, status=status.HTTP_200_OK)
