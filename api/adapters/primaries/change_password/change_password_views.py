# Local utilities
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
from ....adapters.secondaries.factory.constructor_change_password import (
    constructor_change_password as change_password,
)
from apps.backoffice.models import User

from . import change_password_serializer

from ....adapters.secondaries.factory.constructor_email import constructor_user_dashboard as email_sender

emailSender=email_sender()
changePassword=change_password()


class ChangePasswordViewSet(viewsets.GenericViewSet):
    """Vista para cambio de contraseña del usuario"""

    serializer_class = change_password_serializer.ChangePasswordSerializer
    permission_classes = [DjangoModelPermissions]
    queryset = users_models.User.objects.all()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = None
        self.user_email = None

    @swagger_auto_schema(
        operation_summary="Cambio de contraseña",
        operation_description="Servicio para cambio de contraseña por parte del usuario",
        request_body=change_password_serializer.ChangePasswordSerializer(),
        responses={
            status.HTTP_200_OK: "Password cambiado exitosamente",
            status.HTTP_404_NOT_FOUND: "Usuario no encontrado",
            status.HTTP_400_BAD_REQUEST: "Error en la solicitud"
        },
        tags=['Cambiar Contraseña']
    )
    def cambiar_password(self, request) -> Response:
        """Cambiar la contraseña del usuario"""

        serializer = change_password_serializer.ChangePasswordSerializer(data=request.data)
        token = f"Bearer {request.user.open_fin_token}"
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as error_exception:
            return Response({"detail": error_exception.detail}, status=status.HTTP_400_BAD_REQUEST)

        datos = serializer.validated_data

        cambio_password_openfin = changePassword.change_password(
            old_password=datos.get("old_password"),
            new_password=datos.get("new_password"),
            password_confirmation=datos.get("password_confirmation"),
            token=token
        )
        if cambio_password_openfin.get('code') == 200:
            try:
                user = get_object_or_404(users_models.User, email=request.user.email)
                hashed_password = make_password(datos.get("new_password"), hasher="pbkdf2_sha256")
                user.password = hashed_password
                user.save()

                return Response({"detail": "Password cambiado exitosamente"}, status=status.HTTP_200_OK)
            except users_models.User.DoesNotExist:
                return Response({"detail": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "No se pudo cambiar la contraseña en OpenFin."}, status=status.HTTP_400_BAD_REQUEST)

    def get_user_dashboard(self, email):
        """List recipients"""
        user = get_object_or_404(users_models.User, email=email)
        self.username=user.username

