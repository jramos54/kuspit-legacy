"""views for account service"""
# Local utilities
from compartidos.serializers import NotFoundSerializer

# Database imports
from apps.backoffice.models import users as users_models

# Librerías de Terceros
# Django REST Framework
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import viewsets, status

# Third party libraries
from drf_yasg.utils import swagger_auto_schema

# Proyecto
# engine imports
from ....adapters.secondaries.factory import constructor_account as account_repository
from ....adapters.secondaries.factory import constructor_users as users_repo
from ....engine.use_cases import factory as account_engine
from ....engine.use_cases import factory as users_engine
from . import accounts_serializers

# users engine implementation
users_repository = users_repo.constructor_users(users_models.User)
users_engine = users_engine.constructor_manager_users(users_repository)

account_repository = account_repository.constructor_manager_account()
accounts_engine = account_engine.constructor_manager_account(account_repository)


class AccountsViewSet(viewsets.GenericViewSet):
    """Views for accounts service"""

    queryset = users_models.User.objects.all()
    serializer_class = accounts_serializers.AccountsSerializer
    permission_classes = [DjangoModelPermissions]

    @swagger_auto_schema(
        operation_summary="Creacion de una nueva wallet asociada al usuario",
        operation_description="Solicitud de la creacion de una nueva wallet para que se asocie con el usuario",
        request_body=accounts_serializers.AccountsSerializer(),
        responses={
            status.HTTP_200_OK: accounts_serializers.AccountsSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
        tags=['Wallets/Cuentas']

    )
    def create_account(self, request) -> Response:
        """opening account services"""
        data = request.data
        token_openfin = request.user.open_fin_token
        account_serialized = accounts_serializers.AccountsSerializer(data=data)
        account_serialized.is_valid(raise_exception=True)
        # implementation
        account_openfin = accounts_engine.create_account(
            alias=account_serialized.validated_data.get("alias"),
            type_account=account_serialized.validated_data.get("type_account"),
            token=token_openfin,
        )
        try:
            serializer = accounts_serializers.AccountsSerializer(
                data=account_openfin.__dict__
            )
            serializer.is_valid(raise_exception=True)

            message = """
            La cuenta se a creado exitosamente 
            """
            response_data = {
                "detail": message,
                "data": serializer.data,
            }
            return Response(response_data, status.HTTP_201_CREATED)
        except Exception as e:
            print(
                "error al serializar el account, un error o data diferente de openfin"
            )
            data = {
                "detail": "no se pudo dar de alta la cuenta nueva",
                "data": account_openfin,
            }
            print(e)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Listar las wallets de la cuenta del usuario",
        operation_description="Lista las wallets asociadas al usuario para enviar o recibir recursos",
        query_serializer=accounts_serializers.AccountsQueryParamSerializer(),
        responses={
            status.HTTP_200_OK: accounts_serializers.AccountsSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
        tags=['Wallets/Cuentas']

    )
    def list_accounts(self, request):
        """List/Retrieve account service"""
        token_openfin = request.user.open_fin_token
        query_params = request.query_params
        query_serializer = accounts_serializers.AccountsQueryParamSerializer(
            data=query_params
        )
        query_serializer.is_valid(raise_exception=True)
        kauxiliar = query_serializer.validated_data.get("kauxiliar")
        # Filter list by queryparams
        try:
            if kauxiliar is not None:
                account_data = accounts_engine.get_account(
                    kauxiliar=kauxiliar, token=token_openfin
                )
                serializer = accounts_serializers.OpenFinAccountsSerializer(
                    data=account_data.__dict__
                )
                serializer.is_valid(raise_exception=True)
                serialized_data = serializer

                message = """Detalle de wallet"""
                response_data = {"detail": message, "data": serialized_data.data}
                return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response_data = {"detail": "Cuenta no encontrado", "data": ""}
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        list_data = accounts_engine.list_accounts(token=token_openfin)
        serializer = accounts_serializers.OpenFinAccountsSerializer(
            data=list_data, many=True
        )
        serializer.is_valid(raise_exception=True)
        message = """Wallets disponibles"""
        response_data = {
            "detail": message,
            "data": serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)
