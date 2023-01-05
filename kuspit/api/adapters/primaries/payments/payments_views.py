# engine
from api.adapters.secondaries.factory import constructor_payments as payments_repo
from api.engine.use_cases import factory as payments_engine
from api.engine.domain.exceptions import exceptions_customers as exceptions

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.response import Response
# from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import DjangoModelPermissions

from . import payments_serializer
from compartidos.serializers import NotFoundSerializer
from apps.webApp.models import customers as customers_models

# engine implementation
payments_repository = payments_repo.constructor_payments(customers_models.PaymentsCustomer)
payments_engine = payments_engine.constructor_manager_payments(payments_repository)


class CustomersPaymentsViewSet(viewsets.GenericViewSet):
    """
    CustomerPayments CRUD ViewSet
    """

    serializer_class = payments_serializer.PaymentsCustomersSerializer
    permission_classes = [DjangoModelPermissions]
    queryset = customers_models.PaymentsCustomer.objects.all()

    @swagger_auto_schema(
        query_serializer=payments_serializer.CustomerQueryParamsSerializer(),
        responses={
            status.HTTP_200_OK: payments_serializer.PaymentsCustomersSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def list_payments(self, request) -> Response:
        query_params = request.query_params
        query_params_serializer = payments_serializer.CustomerQueryParamsSerializer(
            data=query_params
        )
        query_params_serializer.is_valid(raise_exception=True)

        customer_id = query_params_serializer.validated_data.get("customer_id")

        if customer_id:
            try:
                payments = payments_engine.list_payments(**customer_id)
            except Exception as e:
                print(f"'{e}' exception raised in {__name__} at line 49")
                return Response(
                    data=exceptions.CustomerDoesNotExist(customer_id).message,
                    status=status.HTTP_404_NOT_FOUND,
                )

        else:
            payments = payments_engine.list_payments()

        payments_list_serializer = payments_serializer.PaymentsCustomersSerializer(
            data=payments, many=True
        )
        payments_list_serializer.is_valid(raise_exception=False)

        page = self.paginate_queryset(payments)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(data=payments_list_serializer.data, status=status.HTTP_200_OK)
    