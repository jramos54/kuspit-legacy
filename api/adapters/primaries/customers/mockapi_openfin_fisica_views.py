"""mockapi for customer persona fisica"""
from compartidos.serializers import NotFoundSerializer

# Librerías de Terceros
from rest_framework.response import Response
from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema

# Proyecto
from . import customers_persona_fisica_serializer

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
            "genero": "nobinario",
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


class OpenFinPersonaFisicaViewSet(viewsets.GenericViewSet):
    # permission_classes = [DjangoModelPermissions]
    # queryset = User.objects.all()
    # parser_classes = (JSONParser,)
    """
    MockApi de OpenFin
    """

    @swagger_auto_schema(
        request_body=customers_persona_fisica_serializer.OpenFinPersonaFisicaSerializer(),
        responses={
            status.HTTP_200_OK: customers_persona_fisica_serializer.OpenFinPersonaFisicaSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def openfin_create_customer_pf(self, request) -> Response:
        """
        function to create one customer persona fisica
        in OPEN FIN
        """
        data = request.data
        data_serialized = (
            customers_persona_fisica_serializer.OpenFinPersonaFisicaSerializer(
                data=data
            )
        )
        data_serialized.is_valid(raise_exception=True)
        list_data = LIST_DATA

        # user_id = request.user.id

        data = {
            "id": len(list_data) + 1,
            "informacion_general": data_serialized.validated_data.get(
                "informacion_general"
            ),
        }

        list_data.append(data)

        serializer = customers_persona_fisica_serializer.OpenFinPersonaFisicaSerializer(
            data=data
        )
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        query_serializer=customers_persona_fisica_serializer.OpenFinPersonaFisicaQueryParamsSerializer(),
        responses={
            status.HTTP_200_OK: customers_persona_fisica_serializer.OpenFinPersonaFisicaSerializer(
                many=True
            ),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def openfin_list_customer_pf(self, request) -> Response:
        """fuction for get one customer persona fisica"""
        data = request.query_params
        query_params_serializer = customers_persona_fisica_serializer.OpenFinPersonaFisicaQueryParamsSerializer(
            data=data
        )
        query_params_serializer.is_valid(raise_exception=True)

        user_id = query_params_serializer.validated_data.get("user_id")
        email = query_params_serializer.validated_data.get("email")
        list_data = LIST_DATA

        data = list_data

        try:
            if user_id is not None:
                data = list(filter(lambda x: x.get("user_id") == user_id, list_data))
            elif email is not None:
                data = list(
                    filter(
                        lambda x: x.get("openfin_info").get("email") == email, list_data
                    )
                )
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

        serializer = customers_persona_fisica_serializer.OpenFinPersonaFisicaSerializer(
            data=data, many=True
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=customers_persona_fisica_serializer.OpenFinPersonaFisicaSerializer(),
        query_serializer=customers_persona_fisica_serializer.OpenFinPersonaFisicaQueryParamsSerializer(),
        responses={
            status.HTTP_200_OK: customers_persona_fisica_serializer.OpenFinPersonaFisicaSerializer(
                many=True
            ),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def openfin_update_customer_pf(self, request) -> Response:
        """function to update one customer persona fisica"""
        query_params_serializer = customers_persona_fisica_serializer.OpenFinPersonaFisicaQueryParamsSerializer(
            data=request.data
        )
        query_params_serializer.is_valid(raise_exception=True)

        persona_fisica = request.data
        persona_fisica_serialized = (
            customers_persona_fisica_serializer.OpenFinPersonaFisicaSerializer(
                data=persona_fisica
            )
        )
        persona_fisica_serialized.is_valid(raise_exception=True)

        query_params_serializer.validated_data.get("user_id")
        is_staff = request.user.is_staff
        is_customer = request.user.is_customer

        if is_staff:
            persona_fisica = {
                #'id': len(update_data)+1,
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
            customers_persona_fisica_serializer.OpenFinPersonaFisicaSerializer(
                data=persona_fisica
            )
        )
        customer_serializer.is_valid(raise_exception=True)

        return Response(customer_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        query_serializer=customers_persona_fisica_serializer.OpenFinPersonaFisicaQueryParamsSerializer(),
        responses={
            status.HTTP_200_OK: customers_persona_fisica_serializer.OpenFinPersonaFisicaSerializer(
                many=True
            ),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def openfin_delete_customer_pf(self, request) -> Response:
        """function to update one customer persona fisica"""
        data = request.query_params
        query_params_serializer = customers_persona_fisica_serializer.OpenFinPersonaFisicaQueryParamsSerializer(
            data=data
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
