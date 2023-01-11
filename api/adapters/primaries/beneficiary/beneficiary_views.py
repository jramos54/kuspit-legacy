from compartidos.serializers import NotFoundSerializer

# Librerías de Terceros
from rest_framework.response import Response
from rest_framework import viewsets, status

# Django REST Framework
from drf_yasg.utils import swagger_auto_schema

# Proyecto
from . import beneficiary_serializer

beneficiary_dummy = {
    "openfin_id": 1,
    "idasociado": 1,
    "openfin_info": {
        "nombre": "Arioto",
        "paterno": "Ramos",
        "materno": "Molina",
        "fecha_nacimiento": "2016-11-02",
        "calle": "av evergreen",
        "numext": "3",
        "numint": "0",
        "pais": "Mexico",
        "estado": "estado de Mexico",
        "ciudad": "zumpango",
        "alcaldia": "Zumpango",
        "cp": "55620",
        "parentesco": "perro",
        "porcentaje": 0.99,
    },
}
LIST_DATA = [
    beneficiary_dummy,
]


class BeneficiaryViewSet(viewsets.GenericViewSet):
    """Views for CRUD Beneficiary"""

    serializer_class = beneficiary_serializer.BeneficiarySerializer

    @swagger_auto_schema(
        request_body=beneficiary_serializer.BeneficiarySerializer(),
        responses={
            status.HTTP_200_OK: beneficiary_serializer.BeneficiarySerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def create_beneficiario(self, request) -> Response:
        """dar de alta un beneficiario"""
        data = request.data
        data_serialized = beneficiary_serializer.BeneficiarySerializer(data=data)
        data_serialized.is_valid(raise_exception=True)
        list_data = LIST_DATA

        list_data.append(data_serialized.validated_data)

        serializer = beneficiary_serializer.BeneficiarySerializer(
            data=data_serialized.validated_data
        )
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=beneficiary_serializer.BeneficiaryQueryParamSerializer(),
        responses={
            status.HTTP_200_OK: beneficiary_serializer.BeneficiaryQueryParamSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def update_beneficiario(self, request) -> Response:
        """Update a beneficiary"""
        query_params_serializer = (
            beneficiary_serializer.BeneficiaryQueryParamSerializer(data=request.data)
        )
        query_params_serializer.is_valid(raise_exception=True)

        openfin_id = query_params_serializer.validated_data.get("openfin_id")
        query_params_serializer.validated_data.get("idasociado")
        update_data = LIST_DATA
        elements_update = list(
            filter(lambda x: x.get("openfin_id") == openfin_id, update_data)
        )
        element_update = elements_update[0]

        updated_data = {
            "openfin_info": {
                "nombre": "Arioto",
                "paterno": "Ramos",
                "materno": "Molina",
                "fecha_nacimiento": "2016-11-02",
                "calle": "av evergreen",
                "numext": "3",
                "numint": "0",
                "pais": "Mexico",
                "estado": "estado de Mexico",
                "ciudad": "zumpango",
                "alcaldia": "Zumpango",
                "cp": "55620",
                "parentesco": "perro",
                "porcentaje": 0.99,
            }
        }
        position = update_data.index(element_update)
        update_data[position]["openfin_info"] = updated_data.get("openfin_info")
        instance = update_data[position]["openfin_info"]
        serializer = beneficiary_serializer.BeneficiarySerializer(
            instance,
            data={"alias": update_data[0]["openfin_info"].get("alias")},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=beneficiary_serializer.BeneficiaryQueryParamSerializer(),
        responses={
            status.HTTP_200_OK: beneficiary_serializer.BeneficiaryQueryParamSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def delete_beneficiario(self, request) -> Response:
        """Delete the beneficiario"""
        query_params_serializer = (
            beneficiary_serializer.BeneficiaryQueryParamSerializer(data=request.data)
        )
        query_params_serializer.is_valid(raise_exception=True)

        openfin_id = query_params_serializer.validated_data.get("openfin_id")
        query_params_serializer.validated_data.get("idasociado")

        update_data = LIST_DATA

        elements_update = list(
            filter(lambda x: x.get("openfin_id") == openfin_id, update_data)
        )
        element_update = elements_update[0]

        position = update_data.index(element_update)
        element_deleted = update_data.pop(position)
        # serializer = beneficiary_serializer.BeneficiarySerializer(data=update_data[0])
        # serializer.is_valid(raise_exception=True)

        return Response(element_deleted, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: beneficiary_serializer.BeneficiaryQueryParamSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def list_beneficiario(self, request) -> Response:
        """List Beneficiary"""
        list_data = [LIST_DATA[0]["openfin_info"]]

        list_recipients = beneficiary_serializer.BeneficiarySerializer(
            list_data, many=True
        )
        serialized_data = list_recipients.data

        return Response(serialized_data, status=status.HTTP_200_OK)
