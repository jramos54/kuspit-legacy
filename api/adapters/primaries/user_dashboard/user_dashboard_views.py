# Local utilities
from compartidos.serializers import NotFoundSerializer
from apps.backoffice.models import users as users_models
from apps.backoffice.models.Log2fa_model import Log2FA

# Librerías de Terceros
from rest_framework.permissions import DjangoModelPermissions
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from rest_framework.response import Response
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404

# Proyecto
from ....adapters.secondaries.factory import (
    constructor_user_dashboard as user_dashboard_repository,
)
from ....engine.use_cases.factory import (
    constructor_manager_user_dashboard as user_dashboard_engine,
)
from . import user_dashboard_serializer
from .swagger_docs import ( show_user_data_docs,
                           get_user_by_email_docs,
                           update_2fa_status_docs,
                           update_new_user_status_docs)

users_dashboard_repository = user_dashboard_repository.constructor_user_dashboard()
users_dashboard_engine = user_dashboard_engine(users_dashboard_repository)


class UserDashboardViewSet(viewsets.GenericViewSet):
    """Views for CRUD Recipients"""

    serializer_class = user_dashboard_serializer.UserDashboardSerializer
    permission_classes = [DjangoModelPermissions]
    queryset = users_models.User.objects.all()

    @show_user_data_docs
    def get_user_dashboard(self, request) -> Response:
        """List recipients"""
        token = f"Bearer {request.user.open_fin_token}"
        print(f"OpenFin Token: \n {token}")

        try:
            # Llama al servicio externo para obtener el dashboard del usuario
            user_dashboard_openfin = users_dashboard_engine.get_user_dashboard(
                token=token
            )

            # Serializa los datos obtenidos
            serializer = user_dashboard_serializer.UserDashboardSerializer(
                data=user_dashboard_openfin.__dict__
            )

            # Obtener correo desde el objeto user_dashboard_openfin
            correo = getattr(user_dashboard_openfin, 'correo', None)

            if correo:
                # Utiliza el modelo de usuario personalizado en lugar del modelo predeterminado de Django
                User = get_user_model()

                # Consulta en la tabla de usuarios personalizada para obtener el user_id
                user = User.objects.filter(email=correo).first()

                if user:
                    # Verifica si ya existe un registro en Log2FA
                    log2fa = Log2FA.objects.filter(user=user).first()

                    if not log2fa:
                        # Si no existe, crea un nuevo registro con status_2fa = False
                        log2fa = Log2FA.objects.create(user=user, status_2fa=False)

                    # Consulta en la tabla de grupos para obtener los grupos asociados al user_id
                    groups = Group.objects.filter(user=user)
                    group_names = [group.name for group in groups]

                    # Agrega los grupos y el status_2fa al serializador
                    serializer.initial_data['perfil'] = group_names
                    serializer.initial_data['status_2fa'] = log2fa.status_2fa

                    if serializer.initial_data.get('nombre') != user.username:
                        serializer.initial_data['nombre'] = user.username

                    # Valida los datos serializados
                    serializer.is_valid(raise_exception=True)

                    # Respuesta exitosa
                    response_data = {
                        "detail": "Consulta de usuario exitosa",
                        "data": serializer.data,
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    raise Exception("Usuario no encontrado en la base de datos.")
            else:
                raise Exception("Correo no encontrado en los datos del dashboard.")

        except Exception as error_exception:
            print(error_exception)
            response_data = {"detail": str(error_exception), "data": ""}
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)

    @update_2fa_status_docs
    def update_status_2fa(self, request) -> Response:
        """Update 2FA status"""
        token = f"Bearer {request.user.open_fin_token}"
        print(f"OpenFin Token: \n {token}")

        try:
            # Llama al servicio externo para obtener el dashboard del usuario
            user_dashboard_openfin = users_dashboard_engine.get_user_dashboard(
                token=token
            )

            # Obtener correo desde el objeto user_dashboard_openfin
            correo = getattr(user_dashboard_openfin, 'correo', None)

            if correo:
                # Utiliza el modelo de usuario personalizado en lugar del modelo predeterminado de Django
                User = get_user_model()

                # Consulta en la tabla de usuarios personalizada para obtener el user_id
                user = User.objects.filter(email=correo).first()

                if user:
                    # Verifica si ya existe un registro en Log2FA
                    log2fa = Log2FA.objects.filter(user=user).first()

                    if log2fa:
                        # Cambia el status_2fa al valor opuesto
                        log2fa.status_2fa = not log2fa.status_2fa
                        log2fa.save()
                    else:
                        # Crea un nuevo registro en Log2FA con status_2fa = True
                        log2fa = Log2FA.objects.create(user=user, status_2fa=True)

                    # Serializa los datos obtenidos del servicio externo
                    serializer = user_dashboard_serializer.UserDashboardSerializer(
                        data=user_dashboard_openfin.__dict__
                    )

                    # Consulta en la tabla de grupos para obtener los grupos asociados al user_id
                    groups = Group.objects.filter(user=user)
                    group_names = [group.name for group in groups]

                    # Agrega los grupos y el status_2fa al serializador
                    serializer.initial_data['perfil'] = group_names
                    serializer.initial_data['status_2fa'] = log2fa.status_2fa

                    if serializer.initial_data.get('nombre') != user.username:
                        serializer.initial_data['nombre'] = user.username

                    # Valida los datos serializados
                    serializer.is_valid(raise_exception=True)

                    # Respuesta exitosa con los mismos datos que en get_user_dashboard
                    response_data = {
                        "detail": "Actualización de status 2FA exitosa",
                        "data": serializer.data,
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    raise Exception("Usuario no encontrado en la base de datos.")
            else:
                raise Exception("Correo no encontrado en los datos del dashboard.")

        except Exception as error_exception:
            print(error_exception)
            response_data = {"detail": str(error_exception), "data": ""}
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)


class UserNameViewSet(viewsets.GenericViewSet):
    serializer_class = user_dashboard_serializer.UserDashboardSerializer
    queryset = users_models.User.objects.all()

    @get_user_by_email_docs
    def get_user_by_email(self, request):
        """Get user by email and return full name"""
        email = request.query_params.get('email')

        if not email:
            return Response({"detail": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(users_models.User, email=email)

        # Verifica si ya existe un registro en Log2FA
        log2fa = Log2FA.objects.filter(user=user).first()

        if not log2fa:
            log2fa = Log2FA.objects.create(user=user, status_2fa=False)

        data_response = {
            "email": email,
            "full_name": user.username,
            "is_new_user": user.is_new_user,
            "status_2fa": log2fa.status_2fa if log2fa else None,
        }

        return Response(data_response, status=status.HTTP_200_OK)

    @update_new_user_status_docs
    def change_new_user(self, request):
        """Get user by email, toggle is_new_user status and return full name"""
        email = request.query_params.get('email')

        if not email:
            return Response({"detail": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(users_models.User, email=email)

        # Toggle the is_new_user status
        user.is_new_user = not user.is_new_user
        user.save()

        full_name = f"{user.username}"
        is_new_user = user.is_new_user

        return Response({"email": email, "full_name": full_name, "is_new_user": is_new_user}, status=status.HTTP_200_OK)