import json

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from compartidos.serializers import NotFoundSerializer
from apps.backoffice.models import users as users_models
from django.contrib.auth.hashers import make_password


# Librerías de Terceros
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import viewsets, status,serializers
import random

# Django REST Framework
from drf_yasg.utils import swagger_auto_schema

# Proyecto
from ....adapters.secondaries.factory.constructor_spei_discount import (
    constructor_spei_discount as spei_discount,
)
from apps.backoffice.models import User

from . import spei_discount_serializer
descuento_spei=spei_discount()

class SpeiDiscountViewSet(viewsets.GenericViewSet):
    """Vista para cambio de contraseña del usuario"""

    serializer_class = spei_discount_serializer.SpeiDicountSerializer
    permission_classes = [DjangoModelPermissions]
    queryset = users_models.User.objects.all()

    @swagger_auto_schema(
        operation_summary="Asignacion de cuentas para primer spei",
        operation_description="Se asigna wallet y cuenta destino para el descuento del primer Spei",
        request_body=spei_discount_serializer.SpeiDicountSerializer(),
        responses={
            status.HTTP_200_OK: "Se asignaron las cuentas satisfactoriamente",
            status.HTTP_404_NOT_FOUND: "Cuentas no encontradas",
            status.HTTP_400_BAD_REQUEST: "Error en la solicitud"
        },
        tags=['Configuración']
    )
    def aplica_descuento(self, request) -> Response:
        """Cambiar la contraseña del usuario"""

        serializer = spei_discount_serializer.SpeiDicountSerializer(data=request.data)
        token = f"Bearer {request.user.open_fin_token}"
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as error_exception:
            return Response({"detail": error_exception.detail}, status=status.HTTP_400_BAD_REQUEST)

        datos = serializer.validated_data

        aplica_descuento_openfin = descuento_spei.spei_discount(
            kauxiliar=datos.get("kauxiliar"),
            idcuentab=datos.get("idcuentab"),
            token=token
        )
        if aplica_descuento_openfin.get('code') == 200:
            return Response({"detail": "Cuentas Asignadas exitosamente"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No se pudo asignar las cuentas en OpenFin."}, status=status.HTTP_400_BAD_REQUEST)

    def get_user_dashboard(self, email):
        """List recipients"""
        user = get_object_or_404(users_models.User, email=email)
        self.username=user.username