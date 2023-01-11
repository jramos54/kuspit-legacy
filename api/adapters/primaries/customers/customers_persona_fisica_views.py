"""Views for customer persona fisica API"""

# Local utilities
from compartidos.email_sender.functions import send_email_notification
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
    constructor_persona_fisica as customer_repository,
)
from ....adapters.secondaries.factory import constructor_users as users_repo
from ....engine.use_cases import factory as customer_engine
from ....engine.use_cases import factory as users_engine
from . import customers_persona_fisica_serializer

# users engine implementation
users_repository = users_repo.constructor_users(users_models.User)
users_engine = users_engine.constructor_manager_users(users_repository)

customer_repository = customer_repository.constructor_persona_fisica()
persona_fisica_engine = customer_engine.constructor_manager_persona_fisica(
    customer_repository
)


customer_dummy = {
    "id": 1,
    "user_id": 1,
    "idsucursal": "1",
    "openfin_info": {
        "datos_personales": {
            "nombre": "MARCO",
            "paterno": "AGUILA",
            "materno": "MEDRANO",
            "fecha_nacimiento": "2000-01-01",
            "pais_nacionalidad": "México",
            "nacionalidad": "Mexicana",
            "entidad_de_nacimiento": "Monterrey",
            "genero": "nobinario",
            "telefono": "8117480407",
            "rfc": "1234567890123",
            "regimen_fiscal": "un regimen fiscal",
            "curp": "MGUE746298KFHJE6Y4",
            "cp_fiscal": "uncp",
            "email": "un@email.io",
        },
        "domicilio": {
            "calle": "unacalle",
            "numext": "unnumext",
            "numint": "unnumint",
            "pais": "nombredelpais",
            "estado": "unestado",
            "ciudad": "unacolonia",
            "alcaldia": "unmunicipio",
            "cp": "uncp",
        },
        "propietario_legal": {
            "curp": "MGUE746298KFHJE6Y4",
            "nombre": "MARCO",
            "paterno": "AGUILA",
            "materno": "MEDRANO",
            "fecha_nacimiento": "2000-01-01",
            "pais_nacionalidad": "México",
            "nacionalidad": "Mexicana",
            "entidad_de_nacimiento": "Monterrey",
            "genero": "hola",
            "ocupacion": "plomero",
            "rfc": "MGUAY27498S09",
            "regimen_fiscal": "un regimen fiscal",
            "cp_fiscal": "uncp",
            "domicilio": {
                "calle": "unacalle",
                "numext": "unnumext",
                "numint": "unnumint",
                "pais": "México",
                "estado": "unestado",
                "ciudad": "unacolonia",
                "alcaldia": "unmunicipio",
                "cp": "uncp",
            },
            "telefono": "8117480407",
            "email": "un@email.io",
        },
        "perfil_transaccional": {
            "ocupacion": "plomero",
            "giro": "drogs",
            "actividad": "vender",
            "ingreso_mensual_neto": "24000",
            "fuente_de_ingreso": "soy nini",
            "procedencia_del_recuerso": "un aca",
            "ingresos_al_mes": "23000",
            "operaciones_por_mes": "2",
            "destinatarios_operaciones": "unos destinatarios",
            "proveedores": "un proveedor",
            "cuenta_propia": False,
        },
    },
}

LIST_DATA = [
    customer_dummy,
]


class CustomersPersonaFisicaViewSet(viewsets.GenericViewSet):
    """
    Customer's persona fisica ViewSet
    """

    permission_classes = [DjangoModelPermissions]
    queryset = users_models.User.objects.all()

    @swagger_auto_schema(
        request_body=customers_persona_fisica_serializer.CustomerPersonaFisicaSerializer(),
        responses={
            status.HTTP_200_OK: customers_persona_fisica_serializer.CustomerPersonaFisicaSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def create_customer_persona_fisica(self, request) -> Response:
        """function to create one customer persona fisica"""
        data = request.data
        data_serialized = (
            customers_persona_fisica_serializer.CustomerPersonaFisicaSerializer(
                data=data
            )
        )
        data_serialized.is_valid(raise_exception=True)

        user_id = request.user.id
        request.user.is_staff
        request.user.is_customer

        # We transform data to send to openfin provider
        openfin_payload = {"informacion_general": request.data["openfin_info"]}
        persona_fisica_openfin = persona_fisica_engine.create_persona_fisica(
            info=openfin_payload
        )

        if persona_fisica_openfin["id"] is not None:
            users_engine.update_user(
                id=user_id,
                username=None,
                email=None,
                password=None,
                is_active=None,
                is_staff=None,
                is_superuser=None,
                is_customer=None,
                is_persona_fisica=None,
                is_persona_moral=None,
                open_fin_id=int(persona_fisica_openfin["id"]),
                payments_user_id=None,
                login_attempts=None,
                last_attempt=None,
                location=None,
                location_date=None,
            )

        # send email notification implementation
        response_email = send_email_notification(
            subject="Nuevo cliente",
            body="Se ha registrado un nuevo cliente",
            to=[
                "maguila@nxuni.io",
            ],
        )
        if response_email.status_code != 200:
            return Response(
                {"detail": f"Error {response_email.data} al enviar el correo"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = (
            customers_persona_fisica_serializer.CustomerPersonaFisicaSerializer(
                data=data
            )
        )
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=customers_persona_fisica_serializer.CustomerPersonaFisicaSerializer(),
        query_serializer=customers_persona_fisica_serializer.CustomerQueryParamsSerializer(),
        responses={
            status.HTTP_200_OK: customers_persona_fisica_serializer.CustomerPersonaFisicaSerializer(
                many=True
            ),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def update_customer_persona_fisica(self, request) -> Response:
        """function to update one customer persona fisica"""
        query_params_serializer = (
            customers_persona_fisica_serializer.CustomerQueryParamsSerializer(
                data=request.data
            )
        )
        query_params_serializer.is_valid(raise_exception=True)

        persona_fisica = request.data
        persona_fisica_serialized = (
            customers_persona_fisica_serializer.CustomerPersonaFisicaSerializer(
                data=persona_fisica
            )
        )
        persona_fisica_serialized.is_valid(raise_exception=True)

        query_params_serializer.validated_data.get("user_id")
        is_staff = request.user.is_staff
        is_customer = request.user.is_customer

        if is_staff:
            persona_fisica = {
                # 'id': len(update_data)+1,
                "user_id": query_params_serializer.validated_data.get("user_id"),
                "openfin_info": persona_fisica_serialized.validated_data.get(
                    "openfin_info"
                ),
            }
        elif is_customer:
            token_user_id = request.user.id

            persona_fisica = {
                "user_id": token_user_id,
                "openfin_info": persona_fisica_serialized.validated_data.get(
                    "openfin_info"
                ),
            }
        customer_serializer = (
            customers_persona_fisica_serializer.CustomerPersonaFisicaSerializer(
                data=persona_fisica
            )
        )
        customer_serializer.is_valid(raise_exception=True)

        return Response(customer_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        query_serializer=customers_persona_fisica_serializer.CustomerQueryParamsSerializer(),
        responses={
            status.HTTP_200_OK: customers_persona_fisica_serializer.CustomerPersonaFisicaSerializer(
                many=True
            ),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def delete_customer_persona_fisica(self, request) -> Response:
        """function to update one customer persona fisica"""
        data = request.query_params
        query_params_serializer = (
            customers_persona_fisica_serializer.CustomerQueryParamsSerializer(data=data)
        )
        query_params_serializer.is_valid(raise_exception=True)

        user_id = query_params_serializer.validated_data.get("user_id")
        list_data = LIST_DATA

        try:
            element_selected = list(
                filter(lambda x: x.get("user_id") == user_id, list_data)
            )
            element_deleted = list_data.pop(list_data.index(element_selected[0]))
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

        return Response(element_deleted, status=status.HTTP_200_OK)
