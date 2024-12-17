# Librerias
from compartidos.serializers import NotFoundSerializer
from apps.backoffice.models import users as users_models

# Librerías de Terceros
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema

# Proyecto
from ....adapters.secondaries.factory import constructor_bank as bank_repository
from ....engine.use_cases.factory import constructor_manager_bank as bank_engine
from . import bank_serializer
from .swagger_docs import list_banks_docs

banks_repository = bank_repository.constructor_bank()
banks_engine = bank_engine(banks_repository)


class BanksViewSet(viewsets.GenericViewSet):
    """Methods for Bank Views"""

    serializer_class = bank_serializer.BankSerializer
    permission_classes = [DjangoModelPermissions]
    queryset = users_models.User.objects.all()

    @list_banks_docs
    def list_banks(self, request) -> Response:
        """List banks"""
        token = f"Bearer {request.user.open_fin_token}"
        print(f"OpenFin Token: \n {token}")

        query_param_serializer = bank_serializer.BankQueryParamsSerializer(
            data=request.data
        )
        query_param_serializer.is_valid(raise_exception=True)

        bank_name = request.query_params.get("nombre",None)
        clabe = request.query_params.get("clabe",None)
        print(f"nombre de banco {bank_name}")

        if bank_name is not None:
            bank_openfin = banks_engine.get_bank(nombre=bank_name, token=token)
            print(f"data openfin {bank_openfin}")
            try:
                serializer = bank_serializer.BankSerializer(data=bank_openfin.__dict__)
                serializer.is_valid(raise_exception=True)

                response_data = {"message": "", "data": serializer.data}

                return Response(response_data, status=status.HTTP_200_OK)
            except:
                detail = {
                    "detail": "No se encontro banco"
                }
                return Response(detail, status=status.HTTP_404_NOT_FOUND)

        elif clabe is not None:
            list_banks = banks_engine.list_banks(token=token)
            serializer = bank_serializer.BankSerializer(data=list_banks, many=True)
            serializer.is_valid(raise_exception=True)
            bank_found=self.match_clabe(serializer.data,clabe)

            if bank_found:
                return Response(bank_found, status=status.HTTP_200_OK)
            else:
                detail={
                    "detail":"No se encontro banco"
                }
                return Response(detail, status=status.HTTP_404_NOT_FOUND)

        list_banks = banks_engine.list_banks(token=token)
        serializer = bank_serializer.BankSerializer(data=list_banks, many=True)
        serializer.is_valid(raise_exception=True)
        response_data = {"message": "", "data": serializer.data}

        return Response(response_data, status=status.HTTP_200_OK)

    def match_clabe(self, data_list, clabe):
        # Extraer los primeros 3 caracteres de clabe
        clabe_prefix = clabe[:3]

        # Iterar sobre la lista de diccionarios
        for item in data_list:
            key_str = str(item['key'])
            key_suffix = key_str[-3:]

            if clabe_prefix == key_suffix:
                return item

        return None


# request_body=bank_serializer.BankQueryParamsSerializer(),
