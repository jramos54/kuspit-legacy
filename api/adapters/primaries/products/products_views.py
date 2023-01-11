"""views for account service"""
# Local utilities
from compartidos.serializers import NotFoundSerializer

# database imports
from apps.backoffice.models import users as users_models

# Librerías de Terceros
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import viewsets, status

# Django REST Framework
from drf_yasg.utils import swagger_auto_schema

# Proyecto
# engine imports
from ....adapters.secondaries.factory import constructor_products as product_repository
from ....adapters.secondaries.factory import constructor_users as users_repo
from ....engine.use_cases import factory as product_engine
from ....engine.use_cases import factory as users_engine
from . import products_serializers

# users engine implementation
users_repository = users_repo.constructor_users(users_models.User)
users_engine = users_engine.constructor_manager_users(users_repository)

product_repository = product_repository.constructor_manager_products()
product_engine = product_engine.constructor_manager_products(product_repository)


class ProductsViewSet(viewsets.GenericViewSet):
    queryset = users_models.User.objects.all()
    serializer_class = products_serializers.ProductsSerialazer
    permission_classes = [DjangoModelPermissions]

    @swagger_auto_schema(
        operation_summary="Lista los tipos de wallet disponibles",
        operation_description="Lista los tipos de wallet disponibles",
        query_serializer=products_serializers.ProductsQueryParamSerialazer(),
        responses={
            status.HTTP_200_OK: products_serializers.ProductsSerialazer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
        tags=['Wallets/Cuentas']

    )
    def list_products(self, request):
        """List/Retrieve products service"""
        token_openfin = request.user.open_fin_token
        query_params = request.query_params
        query_serializer = products_serializers.ProductsQueryParamSerialazer(
            data=query_params
        )
        query_serializer.is_valid(raise_exception=True)
        id_product = query_serializer.validated_data.get("idproducto")
        # Filter list by queryparams
        if id_product is not None:
            try:
                product_data = product_engine.get_product(
                    id_product=id_product, token=token_openfin
                )
                serializer = products_serializers.ProductsSerialazer(
                    data=product_data.__dict__
                )
                serializer.is_valid(raise_exception=True)

                message = "El producto se obtuvo exitosamente"
                response_data = {"detail": message, "data": serializer.data}

                return Response(response_data, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                response_data = {"detail": "Producto no encontrado", "data": ""}
                return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        list_data = product_engine.list_products(token=token_openfin)
        serializer = products_serializers.ProductsSerialazer(data=list_data, many=True)
        serializer.is_valid(raise_exception=True)
        message = "El listado de productos fue exitoso"
        response_data = {
            "detail": message,
            "data": serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)
