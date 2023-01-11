from compartidos.serializers import NotFoundSerializer
from apps.backoffice.models import users as users_models
from compartidos.logger import logger

# Librerías de Terceros
import requests, json
from rest_framework.authentication import get_authorization_header
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema
from django.urls import reverse

# Proyecto
from ....adapters.secondaries.factory import constructor_movement as movement_repository
from ....engine.use_cases.factory import constructor_manager_movement as movement_engine
from . import movements_serializer

movements_repository = movement_repository.constructor_movements()
movements_engine = movement_engine(movements_repository)


class MovementsViewSet(viewsets.GenericViewSet):
    """Only list the movements by account"""

    serializer_class = movements_serializer.MovementsSerializer
    permission_classes = [DjangoModelPermissions]
    queryset = users_models.User.objects.all()

    @swagger_auto_schema(
        operation_summary="Listar los movimientos de una wallet",
        operation_description="Lista los movimientos de la wallet, se puede filtrar por tipo de movimiento, estatus y rango de fechas",
        query_serializer=movements_serializer.QueryParamMovementsSerializer(),
        responses={
            status.HTTP_200_OK: movements_serializer.QueryParamMovementsSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
        tags=['Movimientos']

    )
    def list_movements_by_account(self, request):
        logger.info("-" * 30 + "Servicio de Movimientos" + "-" * 30)
        token = f"Bearer {request.user.open_fin_token}"
        logger.info(f"OpenFin Token: \n {token}")

        query_param_serializer = movements_serializer.QueryParamMovementsSerializer(
            data=request.query_params
        )
        try:
            query_param_serializer.is_valid(raise_exception=True)
        except ValidationError as error_exception:
            print((error_exception.detail.get("non_field_errors")[0]))
            return Response(
                {"detail": error_exception.detail.get("non_field_errors")[0]}, status=status.HTTP_400_BAD_REQUEST
            )

        data = query_param_serializer.validated_data

        kauxiliar = data.get("kauxiliar", None)
        movimiento = data.get("movimiento", None)
        estatus = data.get("estatus", None)

        if not MovementsViewSet.account_exist(request, kauxiliar):
            return Response(
                {"detail": "Cuenta no existente"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            movements = movements_engine.list_movements_by_account(token, **data)

            movements_serialized = movements_serializer.MovementsSerializer(
                data=movements, many=True
            )
            movements_serialized.is_valid(raise_exception=True)

            filtered_movements = MovementsViewSet.filter_movements(
                movements_serialized.validated_data, movimiento, estatus
            )

            if movements_serialized.validated_data:
                # print(f"OPEN_FIN: Movements {json.dumps(movements_serialized.validated_data, indent=4)}")

                response_data = {
                    "detail": "Consulta de movimientos exitosa",
                    "data": filtered_movements,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "detail": "No hay Movimientos en el periodo",
                    "data": filtered_movements,
                }
                return Response(response_data, status=status.HTTP_200_OK)

        except Exception as error_exception:
            logger.error(f"Error al consultar movimientos: {str(error_exception)}")
            response_data = {
                "detail": "Hubo un problema para consultar los movimientos",
                "error": str(error_exception),  # Asegurarte de serializar el mensaje de error
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


    @staticmethod
    def account_exist(request, kauxiliar):
        auth = get_authorization_header(request).split()
        token_dyp = None
        if auth and len(auth) == 2:
            token_dyp = auth[1].decode("utf-8")

        accounts_url = request.build_absolute_uri(reverse("accounts"))
        params = {"kauxiliar": kauxiliar}
        headers = {"Authorization": "Bearer " + token_dyp}
        try:
            response = requests.get(accounts_url, params=params, headers=headers)
            accounts_data = response.json()

            if not isinstance(accounts_data.get("data", None), dict):
                return False
            else:
                return True

        except requests.RequestException as e:
            return False

    @staticmethod
    def filter_movements(data, movimiento=None, status=None):
        if movimiento is None and status is None:
            return data

        def match_status(item_status, filter_status):
            if filter_status is None:
                return True

            item_status = item_status.title()
            filter_status = filter_status.title()

            if item_status == filter_status:
                return True
            if filter_status.endswith('o') and item_status == filter_status[:-1] + 'a':
                return True
            if filter_status.endswith('a') and item_status == filter_status[:-1] + 'o':
                return True
            return False

        return [
            item for item in data
            if (movimiento is None or item["movimiento"] == movimiento) and
               match_status(item["estatus"], status)
        ]

