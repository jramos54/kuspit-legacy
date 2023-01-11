# Librerias Estandar
import re

from compartidos.location_swagger_doc import location_header
from compartidos.serializers import NotFoundSerializer
from apps.backoffice.models import users as users_models

# Librerías de Terceros
from django.contrib.auth.hashers import make_password

from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, status
from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone

# Proyecto
# users engine imports
from ....adapters.secondaries.factory import constructor_users as users_repo
from ....engine.domain.exceptions import exceptions_users as exceptions
from ....engine.use_cases import factory as users_engine
from . import users_serializer

# users engine implementation
users_repository = users_repo.constructor_users(users_models.User)
users_engine = users_engine.constructor_manager_users(users_repository)


class PermissionsViewSet(viewsets.GenericViewSet):
    """
    Permissions's profile ViewSet
    """

    serializer_class = users_serializer.PermissionsSerializer
    # permission_classes = [IsAuthenticated, DjangoModelPermissions, AllowAny]
    permission_classes = [DjangoModelPermissions]
    queryset = users_models.User.objects.all()

    @swagger_auto_schema(
        manual_parameters=[location_header],
        responses={
            status.HTTP_200_OK: users_serializer.AdministratorsProfileSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
    )
    def profile_detail(self, request) -> Response:
        user = request.user
        groups = user.groups.prefetch_related("permissions")
        roles = []

        for group in groups:
            group_permissions = [
                permission for permission in group.permissions.values("id", "name")
            ]
            permission_dict = {
                "id": group.id,
                "name": group.name,
                "permissions": group_permissions,
            }
            roles.append(permission_dict)

        profile_info = {
            "id": user.id,
            # "name": user.name,
            "username": user.username,
            "email": user.email,
        }

        admin_data = {
            "profile_info": profile_info,
            "roles": roles,
        }

        profile_serialized = users_serializer.AdministratorsProfileSerializer(
            data=admin_data
        )
        profile_serialized.is_valid(raise_exception=True)

        return Response(data=profile_serialized.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=users_serializer.BaseUserSerializer,
        responses={
            status.HTTP_201_CREATED: users_serializer.BaseUserSerializer(),
            status.HTTP_400_BAD_REQUEST: NotFoundSerializer,
        },
    )
    def create_user(self, request) -> Response:
        user_serialized = users_serializer.NewUserSerializer(data=request.data)
        user_serialized.is_valid(raise_exception=True)

        request_user = request.user

        try:
            # TODO: add this password validation to implementation and handle exception from engine exceptions

            user_email = user_serialized.validated_data.get("correo")
            email_regex = re.escape(user_email)

            password_regex = (
                r"^(?!.*" + email_regex + r")"  # check for user email
                # r'(.)\1{3,}'                                                                            # 3 identical characters
                # r'([a-zA-Z0-9])\1\1\1+'                                                                 # 3 numbers or letters in a row
                r"(?!(.*deposits?o?s?\s+y\s+pagos?)).*"  # depositos y pago
                r"(?!.*(\w)\2{2,}).*"  # 3 identical characters in a row
                # r'.{8,}'                                                                                # password length
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()-_+=\[\]{}|\\:;\'"<>,.?\/]).{8,}$'  # password complexity
            )

            password_input = user_serialized.validated_data.get("password")

            if not re.match(password_regex, password_input):
                return Response(
                    data=exceptions.InvalidPassword().message,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            password = make_password(password=password_input, hasher="pbkdf2_sha256")

            nombre= user_serialized.validated_data.get("nombre")
            paterno= user_serialized.validated_data.get("paterno")
            materno= user_serialized.validated_data.get("materno")

            username=f"{nombre} {paterno} {materno}"

            if user_serialized.validated_data.get("persona_fisica"):
                is_persona_fisica=True
                is_persona_moral=False
            else:
                is_persona_fisica = False
                is_persona_moral = True

            user = users_engine.create_user(
                email=user_serialized.validated_data.get("correo"),
                username=username,
                password=password,
                is_persona_fisica=is_persona_fisica,
                is_persona_moral=is_persona_moral,
            )
            user_dict = user.__dict__

        except exceptions.UserAlreadyExists:
            return Response(
                data=exceptions.UserAlreadyExists(
                    user_serialized.validated_data.get("email")
                ).message,
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_serializer = users_serializer.BaseUserSerializer(data=user_dict)
        user_serializer.is_valid(raise_exception=True)

        return Response(data=user_serializer.data, status=status.HTTP_201_CREATED)
