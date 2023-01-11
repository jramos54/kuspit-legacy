# Local utilities
from compartidos.serializers import NotFoundSerializer
from apps.backoffice.models import users as users_models

# Librerías de Terceros
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import viewsets, status

# Django REST Framework
from drf_yasg.utils import swagger_auto_schema

# Proyecto
from ....adapters.secondaries.factory import (
    constructor_recipient_accounts as recipient_account_repository,
)
from ....engine.use_cases.factory import (
    constructor_manager_recipient_accounts as recipient_account_engine,
)
from ....engine.domain.exceptions import exceptions_recipient_account
from . import recipients_accounts_serializer

recipients_account_repository = (
    recipient_account_repository.constructor_recipient_account()
)
recipients_account_engine = (
    recipient_account_engine.constructor_manager_recipient_account(
        recipients_account_repository
    )
)


class RecipientsAccountViewSet(viewsets.GenericViewSet):
    """Views for CRUD Recipients"""

    serializer_class = recipients_accounts_serializer
    permission_classes = [DjangoModelPermissions]
    queryset = users_models.User.objects.all()

    @swagger_auto_schema(
        operation_summary="Crea una wallet para el destinatario",
        operation_description="Se crea una wallet donde se envian los recusos al destinatario",
        request_body=recipients_accounts_serializer.RecipientAccountSerializer(),
        responses={
            status.HTTP_200_OK: recipients_accounts_serializer.RecipientAccountSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
        tags=['Destinatarios']
    )
    def create_recipient_account(self, request) -> Response:
        """dar de alta un recipient"""
        data = request.data
        data_serialized = recipients_accounts_serializer.RecipientAccountSerializer(
            data=data
        )
        try:
            data_serialized.is_valid(raise_exception=True)
            informacion = data_serialized.data
        # implementacion
        except exceptions_recipient_account.InvalidLenght as e:
            print("error de longitud")
            return Response(e.message, status=status.HTTP_400_BAD_REQUEST)

        token = f"Bearer {request.user.open_fin_token}"
        print(f"esto es el token \n {token}")
        # request a open fin
        try:
            recipient_account_openfin = (
                recipients_account_engine.create_recipient_account(
                    iddestinatario=data["iddestinatario"],
                    institucion_bancaria=informacion["institucion_bancaria"],
                    cuenta=informacion["cuenta"],
                    catalogo_cuenta=informacion["catalogo_cuenta"],
                    limite_operaciones=informacion["limite_operaciones"],
                    is_active=informacion["is_active"],
                    limite=informacion["limite"],
                    alias=informacion["alias"],
                    token=token,
                )
            )
            print(f"respuesta de openfin: {recipient_account_openfin}")
        except KeyError as e:
            print("error en crear cuenta del destinatario por campos faltantes")
            error_type = e.args[0]
            message = {
                "detail": f"no se pudo crear la cuenta del destinatario, falta el campo {error_type}"
            }
            print(message)
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer = recipients_accounts_serializer.RecipientAccountSerializer(
                data=recipient_account_openfin.__dict__
            )
            serializer.is_valid(raise_exception=True)

            message = "La cuenta del destinatario fue dado de alta exitosamente."
            response_data = {
                "detail": message,
                "data": serializer.data,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as error_exception:
            print(
                "error al serializar la cuenta del destinatario, un error o data diferente de openfin"
            )

            data = {
                "detail": recipient_account_openfin.get("message"),
                "data": recipient_account_openfin,
            }

            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Actualiza una cuenta del destinatario",
        operation_description="Se actualizan los datos de wallet del destinatario",
        request_body=recipients_accounts_serializer.RecipientAccountQueryParamSerializer(),
        responses={
            status.HTTP_200_OK: recipients_accounts_serializer.RecipientAccountQueryParamSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
        tags=['Destinatarios']
    )
    def update_recipient_account(self, request) -> Response:
        """Update a recipient"""
        query_params_serializer = (
            recipients_accounts_serializer.RecipientAccountSerializer(data=request.data)
        )
        query_params_serializer.is_valid(raise_exception=True)

        informacion = query_params_serializer.validated_data
        print(informacion)
        token = f"Bearer {request.user.open_fin_token}"
        print(f"esto es el token \n {token}")

        # element_update.update(updated_data)
        recipient_account_openfin = recipients_account_engine.update_recipient_account(
            idcuenta=informacion["idcuenta"],
            is_active=informacion["is_active"],
            limite_operaciones=informacion["limite_operaciones"],
            limite=informacion["limite"],
            alias=informacion["alias"],
            token=token,
        )
        try:
            serializer = recipients_accounts_serializer.RecipientAccountSerializer(
                data=recipient_account_openfin.__dict__
            )
            serializer.is_valid(raise_exception=True)

            response_data = {
                "detail": "Cuenta actualizada correctamente.",
                "data": serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as error_exception:
            print(
                "error al serializar la cuenta del destinatario, un error o data diferente de openfin"
            )

            data = {
                "detail": "La cuenta a modificar no existe",
                "data": recipient_account_openfin,
            }

            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Elimina una wallet del destinatario",
        operation_description="Se elimina la wallet de un destinatario",
        request_body=recipients_accounts_serializer.RecipientAccountQueryParamSerializer(),
        responses={
            status.HTTP_200_OK: recipients_accounts_serializer.RecipientAccountQueryParamSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
        tags=['Destinatarios']
    )
    def delete_recipient_account(self, request) -> Response:
        """Deactivate the recipient"""
        query_params_serializer = (
            recipients_accounts_serializer.RecipientAccountQueryParamSerializer(
                data=request.data
            )
        )
        query_params_serializer.is_valid(raise_exception=True)

        try:
            id_cuenta_openfin = int(request.query_params.get("idcuenta"))
            id_destinatario_openfin = int(request.query_params.get("iddestinatario"))
        except Exception as error_exception:
            response_data = {
                "detail": "Debe indicar cuenta y destinatario valido para poder ser eliminado",
                "data": "",
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        token = f"Bearer {request.user.open_fin_token}"
        print(f"esto es el token \n {token}")
        print(
            f" el idcuenta es {type(id_cuenta_openfin)} y el iddestinatario es {type(id_destinatario_openfin)}"
        )
        delete_account = recipients_account_engine.delete_recipient_account(
            idcuenta=id_cuenta_openfin,
            iddestinatario=id_destinatario_openfin,
            token=token,
        )
        print(f"recived from openfin {delete_account}")
        if delete_account == 404:
            response_data = {
                "detail": "La cuenta o destinatario no existe",
                "data": delete_account,
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        elif delete_account == 200:
            response_data = {
                "detail": "La cuenta ha sido eliminada correctamente",
                "data": delete_account,
            }
            return Response(response_data, status=status.HTTP_200_OK)
