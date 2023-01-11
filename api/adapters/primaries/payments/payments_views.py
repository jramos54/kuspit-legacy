"""views for payments service"""
# Local utilities
from compartidos.serializers import NotFoundSerializer

# Database imports
from apps.backoffice.models import users as users_models

# Librerías de Terceros
# Django REST Framework
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.urls import reverse
import json


# Third party libraries
from drf_yasg.utils import swagger_auto_schema
from django.contrib.gis.geos import Point


# Proyecto
from ....adapters.secondaries.factory import constructor_payments as payment_repository
from ....adapters.secondaries.factory import constructor_users as users_repo
from ....engine.use_cases import factory as payment_engine
from ....engine.use_cases import factory as users_engine
from . import payments_serializer
from ....adapters.secondaries.Geolocation.geolocation_service import GeolocationService
from ....adapters.secondaries.Geolocation.geolocation_serializer import GeolocationSerializer

# engine imports


# users engine implementation
users_repository = users_repo.constructor_users(users_models.User)
users_engine = users_engine.constructor_manager_users(users_repository)

payment_repository = payment_repository.constructor_manager_payments()
payments_engine = payment_engine.constructor_manager_payments(payment_repository)


class PaymentsViewSet(viewsets.GenericViewSet):
    """Views for payments service"""

    queryset = users_models.User.objects.all()
    serializer_class = payments_serializer.PaymentSerializer
    permission_classes = [DjangoModelPermissions]

    geolocation_service = GeolocationService()

    @swagger_auto_schema(
        operation_summary="Se genera un pago a terceros",
        operation_description="Se prepara la generacion de pagos a terceros.",
        request_body=payments_serializer.PaymentSerializer(),
        responses={
            status.HTTP_200_OK: payments_serializer.PaymentSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
        tags=['Pagos']

    )
    def create_payment(self, request) -> Response:
        """opening payment services"""
        data = request.data
        token_openfin = request.user.open_fin_token
        payment_serialized = payments_serializer.PaymentGeolocationSerializer(data=data)
        payment_serialized.is_valid(raise_exception=True)

        geolocalization_data = payment_serialized.validated_data.get("geolocalizacion")

        latitude = float(geolocalization_data.get("latitude", 0))
        longitude = float(geolocalization_data.get("longitude", 0))
        location = Point(longitude, latitude)
        payment_data = payment_serialized.validated_data["payment"]

        # Implementación
        payment_openfin = payments_engine.create_payment(
            kauxiliar=payment_data.get("kauxiliar"),
            id_recipient=payment_data.get("id_recipient"),
            id_account=payment_data.get("id_account"),
            amount=payment_data.get("amount"),
            description=payment_data.get("description"),
            payment_date=payment_data.get("payment_date"),
            reference=payment_data.get("reference"),
            payment_hour=payment_data.get("payment_hour", None),
            token=token_openfin,
        )

        try:

            serializer = payments_serializer.OpenFinPaymentSerializer(
                data=payment_openfin.__dict__
            )
            serializer.is_valid(raise_exception=True)

            message = """
            El pago se ha generado exitosamente 
            """
            response_data = {
                "detail": message,
                "data": serializer.data,
            }
            self.geolocation_service.save_geolocation(
                user=request.user,
                location=location,
                service=json.dumps({"Service": "Payments", "Method": "post", "url": reverse("payment")})
            )
            return Response(response_data, status.HTTP_201_CREATED)

        except Exception as e:
            print(
                "error al serializar el payment, un error o data diferente de openfin"
            )
            data = {
                "detail": "no se pudo programar el pago",
                "data": payment_openfin,
            }
            print(e)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Se lista el historial de pagos",
        operation_description="Se muestra el listado del historial de pagos",
        query_serializer=payments_serializer.PaymentsQueryParamSerializer(),
        responses={
            status.HTTP_200_OK: payments_serializer.OpenFinPaymentSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
        tags=['Pagos']

    )
    def list_payments(self, request):
        """List/Retrieve payment service"""
        token_openfin = request.user.open_fin_token
        query_params = request.query_params
        query_serializer = payments_serializer.PaymentsQueryParamSerializer(
            data=query_params
        )
        query_serializer.is_valid(raise_exception=True)
        date = query_serializer.validated_data.get("defecha")
        to_date = query_serializer.validated_data.get("afecha")

        list_data = payments_engine.list_payments(
            date=date, to_date=to_date, token=token_openfin
        )
        if type(list_data) == dict:
            message = """Sin Historial de pagos"""
            response_data = {
                "detail": message,
                "data": list_data["data"],
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        else:
            list_data = [entidad.__dict__ for entidad in list_data]
            serializer = payments_serializer.OpenFinPaymentSerializer(
                data=list_data, many=True
            )
            serializer.is_valid(raise_exception=True)
            message = """Historial de pagos"""
            response_data = {
                "detail": message,
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Eliminacion de pagos",
        operation_description="Se cancelan los pagos programados",
        query_serializer=payments_serializer.PaymentQueryParamSerializer(),
        responses={
            status.HTTP_200_OK: payments_serializer.PaymentQueryParamSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
        tags=['Pagos']

    )
    def delete_payment(self, request) -> Response:
        """Delete payment"""
        query_params_serializer = payments_serializer.PaymentQueryParamSerializer(
            data=request.query_params
        )
        query_params_serializer.is_valid(raise_exception=True)

        id_transaction = query_params_serializer.validated_data.get("id_transaccion")
        token = f"Bearer {request.user.open_fin_token}"
        print(f"esto es el token \n {token}")

        payment_openfin = payments_engine.delete_payment(
            id_transaction=id_transaction, token=token
        )
        if payment_openfin["code"] == 200:
            data = {
                "detail": "Pago eliminado de forma exitosa",
                "data": payment_openfin,
            }
            return Response(data, status=status.HTTP_200_OK)

        elif payment_openfin["code"] == 400:
            data = {
                "detail": "La eliminacion del pago debe ser por un admin",
                "data": payment_openfin,
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {
                "detail": "El pago no se pudo eliminar o no existe",
                "data": payment_openfin,
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
