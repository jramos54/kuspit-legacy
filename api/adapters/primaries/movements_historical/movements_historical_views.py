# Librerias Estandar
import time

from compartidos.serializers import NotFoundSerializer
from apps.backoffice.models import users as users_models

# Librerías de Terceros
import requests
from rest_framework.authentication import get_authorization_header
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema
from django.urls import reverse

# Proyecto
from ....adapters.secondaries.factory import (
    constructor_movement_historical as movement_repository,
)
from ....engine.use_cases.factory import (
    constructor_manager_movement_by_month as movement_engine,
)
from . import movements_historical_serializer
from .swagger_docs import list_wallet_movements_historical_docs

movements_repository = movement_repository.constructor_movements_historical()
movements_engine = movement_engine(movements_repository)


class MovementsByMonthViewSet(viewsets.GenericViewSet):
    """Only list the movements by account"""

    serializer_class = movements_historical_serializer.MovementsByMonthSerializer
    permission_classes = [DjangoModelPermissions]
    queryset = users_models.User.objects.all()

    @list_wallet_movements_historical_docs
    def list_movements_by_month(self, request):
        start_time = time.time()
        token = f"Bearer {request.user.open_fin_token}"
        print(f"OpenFin Token: \n {token}")
        query_param_serializer = (
            movements_historical_serializer.QueryParamMovementsByMonthSerializer(
                data=request.query_params
            )
        )
        try:
            query_param_serializer.is_valid(raise_exception=True)
        except ValidationError as error_exception:
            return Response(
                {"detail": error_exception.detail}, status=status.HTTP_400_BAD_REQUEST
            )

        data = query_param_serializer.validated_data
        kauxiliar = data.get("kauxiliar", None)

        if not self.account_exist(request, kauxiliar):
            return Response(
                {"detail": "Cuenta no existente"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            # print(" proceso de comunicacion con openfin")
            movements = movements_engine.list_movements_by_month(token, **data)
            movements_serialized = (
                movements_historical_serializer.MovementsByMonthSerializer(
                    data=movements, many=True
                )
            )
            movements_serialized.is_valid(raise_exception=True)
            response_data = {
                "detail": "Consulta de movimientos exitosa",
                "data": movements_serialized.validated_data,
            }
            print(f"tiempo de ejecucion {time.time()-start_time}")
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as error_exception:
            print(error_exception)
            response_data = {
                "detail": "Hubo un problema para consultar los movimientos",
                "data": error_exception,
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def account_exist(self, request, kauxiliar):
        auth = get_authorization_header(request).split()
        token_dyp = None
        if auth and len(auth) == 2:
            token_dyp = auth[1].decode("utf-8")

        accounts_url = request.build_absolute_uri(reverse("accounts"))
        print(accounts_url)
        params = {"kauxiliar": kauxiliar}
        headers = {"Authorization": "Bearer " + token_dyp}
        try:
            response = requests.get(accounts_url, params=params, headers=headers)
            accounts_data = response.json()

            print(f"response de accounts:\n {accounts_data}")
            if not isinstance(accounts_data.get("data", None), dict):
                return False
            else:
                return True

        except requests.RequestException as e:
            return False
