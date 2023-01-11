# Local utilities

from compartidos.serializers import NotFoundSerializer
from apps.backoffice.models import users as users_models
from apps.custom_permissions import IsAdmin, IsSuperUserOrClient
from django.urls import reverse
from rest_framework.test import APIClient



# Librerías de Terceros
from rest_framework.permissions import DjangoModelPermissions,IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.contrib.auth.models import Group
from apps.backoffice.models import User


# Django REST Framework
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Proyecto
from . import operators_serializer
from apps.backoffice.models.roles_model import RolesGroups


from ....adapters.secondaries.factory import (
    constructor_operador as operator_repository,
)
from ....engine.use_cases.factory import (
    constructor_manager_operator as operator_engine,
)

from ....adapters.secondaries.factory.constructor_email import constructor_user_dashboard as email_sender

operators_repository = operator_repository.constructor_operator()
operators_engine = operator_engine(operators_repository)

emailSender=email_sender()


class OperatorsViewSet(viewsets.GenericViewSet):
    """Vista para operaciones CRUD en Recipients"""

    # Define la clase serializer a utilizar
    serializer_class = operators_serializer.OperatorSerializer
    # Define las clases de permisos requeridas para esta vista
    permission_classes = [DjangoModelPermissions,IsAuthenticated]
    # Define el conjunto de consultas para recuperar usuarios
    queryset = users_models.User.objects.all()

    def __int__(self):
        # Inicializa las variables de instancia para el nombre de usuario y el correo electrónico
        self.username = None
        self.user_email = None

    def get_permissions(self):
        if self.action == 'show_operator':
            self.permission_classes = [IsSuperUserOrClient | IsAdmin]
        elif self.action == 'create_operator':
            self.permission_classes = [IsSuperUserOrClient | IsAdmin]
        elif self.action == 'grant_access':
            self.permission_classes = [IsSuperUserOrClient | IsAdmin]
        elif self.action == 'assign_roles':
            self.permission_classes = [IsSuperUserOrClient | IsAdmin]
        return super().get_permissions()

    @swagger_auto_schema(
        request_body=operators_serializer.NuevoOperadorSerializer(),
        responses={
            status.HTTP_200_OK: operators_serializer.OperatorSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
        tags=['Operadores/Perfiles']
    )
    def create_operator(self, request) -> Response:
        """Crear un nuevo destinatario"""
        data_serializer = operators_serializer.NuevoOperadorSerializer(data=request.data)

        try:
            data_serializer.is_valid(raise_exception=True)
            params = data_serializer.data
        except Exception as error_exception:
            data_response = {
                "detail": "error en los parametros de la solicitud"
            }
            return Response(data_response, status=status.HTTP_400_BAD_REQUEST)

        token = f"Bearer {request.user.open_fin_token}"

        operator_openfin = operators_engine.create_operator(
            nombre=params.get("nombre"),
            paterno=params.get("paterno"),
            materno=params.get("materno"),
            correo=params.get("correo"),
            pfisica=params.get("pfisica"),
            password="Demo$1234",
            token=token,
        )
        print(params.get("pfisica"))
        try:
            permissions_data = operators_serializer.PermissionsOperatorSerializer(operator_openfin.permisos.__dict__)
            operator_data = operator_openfin.__dict__
            print(f"operador data es {operator_data}")
            operator_data['permisos'] = permissions_data.data

            operator_serializer = operators_serializer.OperatorSerializer(data=operator_data)
            operator_serializer.is_valid(raise_exception=True)

            create_user_url = reverse('create-user')
            client = APIClient()
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                # Establece el token en los headers
                client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

            payload={
                "password": "Demo$1234",
                "nombre": params.get("nombre"),
                "paterno": params.get("paterno"),
                "materno": params.get("materno"),
                "correo": params.get("correo"),
                "persona_fisica": params.get("pfisica")
            }
            print(payload)
            response = client.post(create_user_url, data=payload, format='json')
            print(response.data)

            message = "Se creo el operador exitosamente"
            response_data = {
                "detail": message,
                "data": operator_serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as error_exception:
            data = {
                "detail": "No se puede crear el operador",
                "data": str(error_exception),
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Asignar o revocar acceso del operador a la cuenta",
        operation_description="",
        request_body=operators_serializer.OperatorSerializer(),
        query_serializer=operators_serializer.OperatorQueryParamSerializer(),
        responses={
            status.HTTP_200_OK: operators_serializer.OperatorSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
        tags=['Operadores/Perfiles']
    )
    def grant_access(self, request) -> Response:
        """Update a recipient"""
        data_serializer = operators_serializer.OperatorQueryParamSerializer(data=request.query_params)

        try:
            data_serializer.is_valid(raise_exception=True)
            params = data_serializer.data
        except Exception as error_exception:
            data_response = {
                "detail": "error en los parametros de la solicitud"
            }
            return Response(data_response, status=status.HTTP_400_BAD_REQUEST)

        token = f"Bearer {request.user.open_fin_token}"

        operator_openfin = operators_engine.grant_access(
            idoperador=params["idoperador"],
            token=token,
        )
        print(f"Views grant_access operator_openfin {operator_openfin}")

        try:
            permissions_data = operators_serializer.PermissionsOperatorSerializer(operator_openfin.permisos.__dict__)
            operator_data = operator_openfin.__dict__
            operator_data['permisos'] = permissions_data.data

            operator_serializer = operators_serializer.OperatorSerializer(data=operator_data)
            operator_serializer.is_valid(raise_exception=True)

            message = "Se dio acceso al operador"
            response_data = {
                "detail": message,
                "data": operator_serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as error_exception:
            data = {
                "detail": "No se puede dar acceso al operador",
                "data": str(error_exception),
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Listar los operadores y rol en la cuenta",
        operation_description="Se listan los operadores por idoperador o todos los registrados en la cuenta",
        responses={
            status.HTTP_200_OK: operators_serializer.OperatorSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
        tags=['Operadores/Perfiles']
    )
    def show_operator(self, request) -> Response:
        """List recipients"""
        token = f"Bearer {request.user.open_fin_token}"
        print(f"OpenFin Token: \n {token}")
        query_param_serializer = operators_serializer.OperatorQueryParamSerializer(
            data=request.query_params
        )
        query_param_serializer.is_valid(raise_exception=True)
        idoperador = query_param_serializer.validated_data.get("idoperador")
        if idoperador is not None:
            operator_openfin = operators_engine.get_operator(
                idoperador=idoperador, token=token
            )

            try:
                permissions_data = operators_serializer.PermissionsOperatorSerializer(
                    operator_openfin.permisos.__dict__)
                operator_data = operator_openfin.__dict__

                permisos_data = permissions_data.data
                if "DYPFE" in permisos_data.get("descripcion", ""):
                    permisos_data["descripcion"] = permisos_data["descripcion"].replace("DYPFE", "").strip()

                operator_data['permisos'] = permisos_data

                operator_serializer = operators_serializer.OperatorSerializer(data=operator_data)
                operator_serializer.is_valid(raise_exception=True)

                response_data = {
                    "detail": "Consulta de operador exitosa",
                    "data": [operator_serializer.data],
                }

                return Response(response_data, status=status.HTTP_200_OK)

            except Exception as error_exception:
                response_data = {"detail": "Operador no encontrado", "data": ""}
                return Response(response_data, status=status.HTTP_403_FORBIDDEN)

        list_operators = operators_engine.list_operator(token=token)
        serialized_operators = []

        try:
            for operator in list_operators:
                permissions_data = operators_serializer.PermissionsOperatorSerializer(operator.permisos.__dict__)
                operator_data = operator.__dict__

                permisos_data = permissions_data.data
                if "DYPFE" in permisos_data.get("descripcion", ""):
                    permisos_data["descripcion"] = permisos_data["descripcion"].replace("DYPFE", "").strip()

                operator_data['permisos'] = permisos_data

                operator_serializer = operators_serializer.OperatorSerializer(data=operator_data)
                operator_serializer.is_valid(raise_exception=True)
                serialized_operators.append(operator_serializer.data)

            response_data = {
                "detail": "Consulta de operadores exitosa",
                "data": serialized_operators,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as error_exception:
            response_data = {"detail": "Operadores no encontrados", "data": ""}
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)

    @swagger_auto_schema(
        operation_summary="Asignar o revocar roles a un operador",
        operation_description="Este endpoint permite asignar o revocar roles a un operador específico dentro del sistema.",
        request_body=operators_serializer.OperatorQueryParamSerializer,
        responses={
            status.HTTP_200_OK: operators_serializer.OperatorSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
            status.HTTP_403_FORBIDDEN: openapi.Response(description="Operator not found")
        },
        tags=['Operadores/Perfiles']

    )
    def assign_roles(self, request) -> Response:
        """Asignar o revocar roles a un operador"""
        token = f"Bearer {request.user.open_fin_token}"
        print(f"OpenFin Token: \n {token}")
        data_serializer = operators_serializer.OperatorQueryParamSerializer(
            data=request.data
        )
        data_serializer.is_valid(raise_exception=True)

        idoperador = data_serializer.validated_data.get("idoperador")
        perfil = data_serializer.validated_data.get("perfil")
        tipo_acceso = data_serializer.validated_data.get("tipo_acceso")

        perfil_mapping = {
            "dypfe_admin": "dypfe_admin",
            "dypfe_tesorero": "dypfe_autorizador",
            "dypfe_analista": "dypfe_analista",
            "dypfe_user": "dypfe_user",
        }

        # Realiza el mapeo del perfil
        perfil_mapeado = perfil_mapping.get(perfil, perfil)

        operator_openfin=None
        mensaje=""
        if tipo_acceso == "quitar":
            operator_openfin = operators_engine.revoke_role(
                idoperador=idoperador,perfil=perfil_mapeado, token=token
            )
            mensaje="Se quito el rol exitosamente"
        elif tipo_acceso == "asignar":
            operator_openfin = operators_engine.assign_role(
                idoperador=idoperador, perfil=perfil_mapeado, token=token
            )
            mensaje="Se asigno el rol exitosamente"

        self.update_user_group(operator_openfin.email,operator_openfin.permisos.perfil)

        try:
            permissions_data = operators_serializer.PermissionsOperatorSerializer(
                operator_openfin.permisos.__dict__)
            operator_data = operator_openfin.__dict__
            operator_data['permisos'] = permissions_data.data

            operator_serializer = operators_serializer.OperatorSerializer(data=operator_data)
            operator_serializer.is_valid(raise_exception=True)

            response_data = {
                "detail": mensaje,
                "data": [operator_serializer.data],
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as error_exception:
            response_data = {"detail": "No se pude asignar un rol al Operador", "data":error_exception }
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)

    @swagger_auto_schema(
        operation_summary="Listar los roles disponibles",
        operation_description="Lista los roles disponibles",
        responses={
            status.HTTP_200_OK: operators_serializer.RolesGroupsSerializer,
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
            status.HTTP_403_FORBIDDEN: openapi.Response(description="Operator not found")
        },
        tags=['Operadores/Perfiles']

    )
    def list_roles(self, request) -> Response:
        """Asignar o revocar roles a un operador"""
        roles_group=RolesGroups.objects.all()
        serializer=operators_serializer.RolesGroupsSerializer(roles_group,many=True)
        data={
            "detail":"Roles disponibles",
            "data":serializer.data

        }
        return Response(data, status=status.HTTP_200_OK)

    def update_user_group(self, email, perfil):
        try:
            user = User.objects.get(email=email)

            # Limpiar todos los grupos del usuario y asignar solo el nuevo perfil
            user.groups.clear()

            if perfil not in ['Sin_Perfil', 'Sin_Acceso']:
                try:
                    group = Group.objects.get(name=perfil)
                    user.groups.add(group)  # Agregar el nuevo perfil como grupo
                except Group.DoesNotExist:
                    print(f"Grupo con nombre {perfil} no encontrado")
                    return

        except User.DoesNotExist:
            print(f"Usuario con email {email} no encontrado")
        except Exception as e:
            print(f"Error actualizando los grupos del usuario: {str(e)}")

    # def get_user_dashboard(self,token) -> Response:
    #     """List recipients"""
    #
    #     try:
    #         user_dashboard_openfin = users_dashboard_engine.get_user_dashboard(
    #              token=token
    #         )
    #
    #         data=user_dashboard_openfin.__dict__
    #         self.username=data.get("nombre")
    #         self.user_email=data.get("correo")
    #
    #     except Exception as error_exception:
    #         print(error_exception)
    #         response_data = {"detail": "Usuario no encontrado", "data": ""}
    #         return response_data

