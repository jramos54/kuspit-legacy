"""Views for customer persona moral API"""
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
    constructor_persona_moral as customer_repository,
)
from ....adapters.secondaries.factory import constructor_users as users_repo
from ....engine.use_cases import factory as customer_engine
from ....engine.use_cases import factory as users_engine
from . import customers_persona_moral_serializer

# users engine implementation
users_repository = users_repo.constructor_users(users_models.User)
users_engine = users_engine.constructor_manager_users(users_repository)

customer_repository = customer_repository.constructor_persona_moral()
persona_moral_engine = customer_engine.constructor_manager_persona_moral(
    customer_repository
)

customer_dummy = {
    "id": 1,
    "user_id": 1,
    "idsucursal": "1",
    "openfin_info": {
        "datos_empresa": {
            "razon_social": "una razon social",
            "nacionalidad": "una nacinalidad",
            "rfc": "un rfc",
            "num_ser_fir_elec": "2343534235345",
            "giro_mercantil": "un giro mercantil",
        },
        "escritura_constitutiva": {
            "fecha_constitucion": "2000-01-01",
            "num_escritura": "666",
            "fecha_protocolizacion": "2000-01-01",
            "rfc": "un rfc",
            "curp": "un curp",
        },
        "representante_legal": {
            "nombre": "MARCO",
            "paterno": "AGUILA",
            "materno": "MEDRANO",
            "email": "postcj@io.com",
            "num_escr_pub": "21874983",
            "fecha_protocolizacion": "2000-01-01",
            "firma_autografa": "una firma",
            "clave_lada": "098762034957603786",
            "telefono": "8972634958629348",
            "extencion": "234",
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
        "otros_datos_personales": {
            "numero_de_cuenta": "123412354123",
            "clave_bancaria": "231423412435",
            "institucion_financiera": "bbva",
            "nombre_comercial": "un nombre comercial",
            "actividades_y_otros": "una actividad y otros",
            "corroborar_datos": "un corroborar datos",
            "clave_bancaria_digitalizada": "123412452345",
            "institucion_financiera_digitalizada": "bbvax2",
            "firma_digitalizada": "una firma bien perrona",
        },
        "datos_de_contacto": {
            "email": "postcj@io.com",
            "telefono": "8972634958629348",
            "razon_social": "una razon social",
            "rfc": "un rfc",
            "nombre": "MARCO",
            "paterno": "AGUILA",
            "materno": "MEDRANO",
        },
    },
}

# customer_dummy = {
#     "id": 1,
#     'user_id': 1,
#     'openfin_info': {
#         'idsucursal': '1',
#         'idrol': '10',
#         'empresa': 'MiCa SA',
#         'domicilio': {
#             'calle': 'Avenida siempre viva',
#             'numext': '666',
#             'numint': '69',
#             'colonia': 'Tepojaco',
#             'municipio': 'Ecatepec',
#             'cp': '00069',
#             'estado': 'Mexico',
#             'entrecalles': 'Entre calle 1 y Calle 2',
#             'pais': 'Mexico'
#         },
#         'telefono': '1234567890',
#         'fecha_constitucion': '30/09/1992',
#         'pais_nacionalidad': 'Mexico',
#         'rfc': 'MIC000101OGT',
#         'idgiro': '1'
#     }
# }
LIST_DATA = [
    customer_dummy,
]


class CustomerPersonaMoralViewSet(viewsets.GenericViewSet):
    """
    Customer's persona moral ViewSet
    """

    permission_classes = [DjangoModelPermissions]
    queryset = users_models.User.objects.all()
    serializer_class = customers_persona_moral_serializer.CustomerPersonaMoralSerializer

    @swagger_auto_schema(
        request_body=customers_persona_moral_serializer.CustomerPersonaMoralSerializer,
        responses={
            status.HTTP_200_OK: customers_persona_moral_serializer.CustomerPersonaMoralSerializer,
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def create_customer_persona_moral(self, request) -> Response:
        """function to create one customer persona fisica"""
        data = request.data
        data_serialized = (
            customers_persona_moral_serializer.CustomerPersonaMoralSerializer(data=data)
        )
        data_serialized.is_valid(raise_exception=True)

        user_id = request.user.id
        request.user.is_staff
        request.user.is_customer

        openfin_payload = {"informacion_general": request.data["openfin_info"]}
        persona_moral_openfin = persona_moral_engine.create_persona_moral(
            info=openfin_payload
        )
        if persona_moral_openfin["id"] is not None:
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
                open_fin_id=int(persona_moral_openfin["id"]),
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

        serializer = customers_persona_moral_serializer.CustomerPersonaMoralSerializer(
            data=data
        )
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        query_serializer=customers_persona_moral_serializer.CustomerQueryParamsSerializer(),
        responses={
            status.HTTP_200_OK: customers_persona_moral_serializer.CustomerPersonaMoralSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def update_customer_persona_moral(self, request) -> Response:
        """function to update one customer persona moral"""
        query_params_serializer = (
            customers_persona_moral_serializer.CustomerQueryParamsSerializer(
                data=request.data
            )
        )
        query_params_serializer.is_valid(raise_exception=True)

        persona_moral = request.data
        persona_moral_serialized = (
            customers_persona_moral_serializer.CustomerPersonaMoralSerializer(
                data=persona_moral
            )
        )
        persona_moral_serialized.is_valid(raise_exception=True)

        query_params_serializer.validated_data.get("user_id")
        is_staff = request.user.is_staff
        is_customer = request.user.is_customer

        if is_staff:
            persona_moral = {
                # 'id': len(update_data)+1,
                "user_id": query_params_serializer.validated_data.get("user_id"),
                "openfin_info": persona_moral_serialized.validated_data.get(
                    "openfin_info"
                ),
            }
        elif is_customer:
            token_user_id = request.user.id

            persona_moral = {
                "user_id": token_user_id,
                "openfin_info": persona_moral_serialized.validated_data.get(
                    "openfin_info"
                ),
            }
        customer_serializer = (
            customers_persona_moral_serializer.CustomerPersonaMoralSerializer(
                data=persona_moral
            )
        )
        customer_serializer.is_valid(raise_exception=True)

        return Response(customer_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        query_serializer=customers_persona_moral_serializer.CustomerQueryParamsSerializer(),
        responses={
            status.HTTP_200_OK: customers_persona_moral_serializer.CustomerPersonaMoralSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def delete_customer_persona_moral(self, request) -> Response:
        """function to delete one customer persona moral"""
        query_params_serializer = (
            customers_persona_moral_serializer.CustomerQueryParamsSerializer(
                data=request.data
            )
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
