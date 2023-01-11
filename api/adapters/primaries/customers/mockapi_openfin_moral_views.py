"""mockapi for customer persona moral"""
from compartidos.serializers import NotFoundSerializer

# Librerías de Terceros
from rest_framework.response import Response
from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema

# Proyecto
from . import customers_persona_moral_serializer

customer_dummy = {
    "id": 1,
    "user_id": 1,
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


class OpenFinPersonaMoralViewSet(viewsets.GenericViewSet):
    # permission_classes = [DjangoModelPermissions]
    # queryset = User.objects.all()
    # parser_classes = (JSONParser,)
    """
    MockApi de OpenFin
    """

    @swagger_auto_schema(
        request_body=customers_persona_moral_serializer.CustomerPersonaMoralSerializer(),
        responses={
            status.HTTP_200_OK: customers_persona_moral_serializer.CustomerPersonaMoralSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def openfin_create_customer_pm(self, request) -> Response:
        """
        function to create one customer persona moral
        in OPEN FIN
        """
        data = request.data
        data_serialized = (
            customers_persona_moral_serializer.OpenFinPersonaMoralSerializer(data=data)
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

        serializer = customers_persona_moral_serializer.OpenFinPersonaMoralSerializer(
            data=data
        )
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        query_serializer=customers_persona_moral_serializer.OpenFinPersonaMoralQueryParamsSerializer(),
        responses={
            status.HTTP_200_OK: customers_persona_moral_serializer.OpenFinPersonaMoralSerializer(
                many=True
            ),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def openfin_list_customer_pm(self, request) -> Response:
        """fuction for get one customer persona moral"""
        data = request.query_params
        query_params_serializer = (
            customers_persona_moral_serializer.OpenFinPersonaMoralQueryParamsSerializer(
                data=data
            )
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

        serializer = customers_persona_moral_serializer.OpenFinPersonaMoralSerializer(
            data=data, many=True
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=customers_persona_moral_serializer.OpenFinPersonaMoralSerializer(),
        query_serializer=customers_persona_moral_serializer.OpenFinPersonaMoralQueryParamsSerializer(),
        responses={
            status.HTTP_200_OK: customers_persona_moral_serializer.OpenFinPersonaMoralSerializer(
                many=True
            ),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def openfin_update_customer_pm(self, request) -> Response:
        """function to update one customer persona moral"""
        query_params_serializer = (
            customers_persona_moral_serializer.OpenFinPersonaMoralQueryParamsSerializer(
                data=request.data
            )
        )
        query_params_serializer.is_valid(raise_exception=True)

        persona_moral = request.data
        persona_moral_serialized = (
            customers_persona_moral_serializer.OpenFinPersonaMoralSerializer(
                data=persona_moral
            )
        )
        persona_moral_serialized.is_valid(raise_exception=True)

        query_params_serializer.validated_data.get("user_id")
        is_staff = request.user.is_staff
        is_customer = request.user.is_customer

        if is_staff:
            persona_moral = {
                #'id': len(update_data)+1,
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
            customers_persona_moral_serializer.OpenFinPersonaMoralSerializer(
                data=persona_moral
            )
        )
        customer_serializer.is_valid(raise_exception=True)

        return Response(customer_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        query_serializer=customers_persona_moral_serializer.OpenFinPersonaMoralQueryParamsSerializer(),
        responses={
            status.HTTP_200_OK: customers_persona_moral_serializer.OpenFinPersonaMoralSerializer(
                many=True
            ),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def openfin_delete_customer_pm(self, request) -> Response:
        """function to update one customer persona moral"""
        data = request.query_params
        query_params_serializer = (
            customers_persona_moral_serializer.OpenFinPersonaMoralQueryParamsSerializer(
                data=data
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
