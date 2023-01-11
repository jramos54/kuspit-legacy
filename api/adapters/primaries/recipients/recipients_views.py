# Local utilities
import json

from compartidos.serializers import NotFoundSerializer
from apps.backoffice.models import users as users_models
from django.urls import reverse


# Librerías de Terceros
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework import viewsets, status

# Django REST Framework
from drf_yasg.utils import swagger_auto_schema
from django.contrib.gis.geos import Point

# Proyecto
from ....adapters.secondaries.factory import (
    constructor_recipient as recipient_repository,
)
from ....engine.use_cases.factory import (
    constructor_manager_recipient as recipient_engine,
)
from ....engine.domain.exceptions import exceptions_recipient
from ....engine.domain.messages import messages_recipients

from . import recipients_serializer

from ....adapters.secondaries.factory import (
    constructor_user_dashboard as user_dashboard_repository,
)
from ....engine.use_cases.factory import (
    constructor_manager_user_dashboard as user_dashboard_engine,
)

from ....adapters.secondaries.factory.constructor_email import constructor_user_dashboard as email_sender
from ....adapters.secondaries.Geolocation.geolocation_service import GeolocationService
from ....adapters.secondaries.Geolocation.geolocation_serializer import GeolocationSerializer

recipients_repository = recipient_repository.constructor_recipient()
recipients_engine = recipient_engine(recipients_repository)

users_dashboard_repository = user_dashboard_repository.constructor_user_dashboard()
users_dashboard_engine = user_dashboard_engine(users_dashboard_repository)

emailSender=email_sender()

class RecipientsViewSet(viewsets.GenericViewSet):
    """Vista para operaciones CRUD en Recipients"""

    # Define la clase serializer a utilizar
    serializer_class = recipients_serializer.RecipientSerializer
    # Define las clases de permisos requeridas para esta vista
    permission_classes = [DjangoModelPermissions]
    # Define el conjunto de consultas para recuperar usuarios
    queryset = users_models.User.objects.all()
    geolocation_service = GeolocationService()
    def __int__(self):
        # Inicializa las variables de instancia para el nombre de usuario y el correo electrónico
        self.username = None
        self.user_email = None

    @swagger_auto_schema(
        operation_summary="Creacion de un destinatario nuevo",
        operation_description="Se realiza el alta de un destinatario en la cuenta",
        request_body=recipients_serializer.DestinatarioSerializer(),
        responses={
            status.HTTP_200_OK: recipients_serializer.RecipientSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
        tags=['Destinatarios']
    )
    def create_recipient(self, request) -> Response:
        """Crear un nuevo destinatario"""

        data = request.data  # Obtiene los datos de la solicitud

        # Deserializa los datos
        data_serialized = recipients_serializer.RecipientGeolocationSerializer(data=data)
        try:
            data_serialized.is_valid(raise_exception=True)  # Valida los datos
            informacion = data_serialized.data  # Extrae los datos validados

        except exceptions_recipient.InvalidRFC as error_exception:
            # Maneja la excepción de RFC inválido
            return Response(error_exception.message, status=status.HTTP_400_BAD_REQUEST)

        except exceptions_recipient.InvalidCURP as error_exception:
            # Maneja la excepción de CURP inválido
            return Response(error_exception.message, status=status.HTTP_400_BAD_REQUEST)

        geolocalization_data = data_serialized.validated_data.get("geolocalizacion")

        latitude = float(geolocalization_data.get("latitude") or 0)
        longitude = float(geolocalization_data.get("longitude") or 0)
        location = Point(longitude, latitude)

        # Genera el token de autorización
        token = f"Bearer {request.user.open_fin_token}"

        # Solicita el panel de control del usuario a Open Fin usando el token
        self.get_user_dashboard(token)

        try:
            # Asegura que los campos RFC y CURP no estén vacíos
            if not informacion.get("rfc"):
                informacion["rfc"] = ""
            elif not informacion.get("curp"):
                informacion["curp"] = ""

            # Crea el destinatario usando el motor de recipients
            recipient_openfin = recipients_engine.create_recipient(
                nombre=informacion["nombre"],
                paterno=informacion["paterno"],
                materno=informacion["materno"],
                rfc=informacion["rfc"],
                curp=informacion["curp"],
                is_active=informacion["is_active"],
                correo=informacion["correo"],
                pfisica=informacion["pfisica"],
                token=token,
            )

        except KeyError as error_exception:
            # Maneja el error de campos faltantes
            print("Error al crear el destinatario debido a campos faltantes")
            error_type = error_exception.args[0]
            message = {
                "detail": f"No se pudo dar de alta el destinatario, falta el campo {error_type}"
            }
            print(message)
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Serializa los datos del destinatario
            serializer = recipients_serializer.RecipientSerializer(
                data=recipient_openfin.__dict__
            )
            print(json.dumps(recipient_openfin.__dict__))
            serializer.is_valid(raise_exception=True)  # Valida los datos serializados

            # Prepara el mensaje de respuesta de éxito
            message = "El destinatario fue dado de alta exitosamente. Puedes realizarle transferencias después de los 30 minutos."
            response_data = {
                "detail": message,
                "data": serializer.data,
            }
            # Prepara el nombre del destinatario para el correo electrónico
            destinatario = f"{recipient_openfin.__dict__.get('nombre')} {recipient_openfin.__dict__.get('paterno')} {recipient_openfin.__dict__.get('materno')}"

            # Crea y envía el correo electrónico de notificación
            messages = messages_recipients.RecipientMessages()
            message_sent = messages.new_recipient_message(self.username, self.user_email, destinatario)
            emailSender.send_email(self.user_email, message_sent.get("asunto"), message_sent.get("mensaje"), token)

            self.geolocation_service.save_geolocation(
                user=request.user,
                location=location,
                service=json.dumps({"Service": "Recipient", "Method": "post", "url": reverse("recipients")})
            )

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as error_exception:
            # Maneja errores genéricos durante la serialización
            print("Error al serializar el destinatario, o datos diferentes de OpenFin")
            data = {
                "detail": "No se pudo dar de alta el destinatario",
                "data": recipient_openfin,
            }
            print(error_exception)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Actualizacion de un destinatario existente",
        operation_description="Se realiza la actualizacion de datos de un destinatario existente",
        request_body=recipients_serializer.RecipientSerializer(),
        query_serializer=recipients_serializer.RecipientQueryParamSerializer(),
        responses={
            status.HTTP_200_OK: recipients_serializer.RecipientQueryParamSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
        tags=['Destinatarios']
    )
    def update_recipient(self, request) -> Response:
        """Update a recipient"""
        data_serializer = recipients_serializer.RecipientGeolocationSerializer(data=request.data)

        try:
            data_serializer.is_valid(raise_exception=True)
            informacion = data_serializer.data

        except exceptions_recipient.InvalidRFC as error_exception:
            return Response(error_exception.message, status=status.HTTP_400_BAD_REQUEST)

        except exceptions_recipient.InvalidCURP as error_exception:
            return Response(error_exception.message, status=status.HTTP_400_BAD_REQUEST)

        geolocalization_data = data_serializer.validated_data.get("geolocalizacion")

        latitude = float(geolocalization_data.get("latitude") or 0)
        longitude = float(geolocalization_data.get("longitude") or 0)
        location = Point(longitude, latitude)

        # informacion = data_serializer.validated_data
        token = f"Bearer {request.user.open_fin_token}"

        recipient_openfin = recipients_engine.update_recipient(
            iddestinatario=informacion["iddestinatario"],
            nombre=informacion["nombre"],
            paterno=informacion["paterno"],
            materno=informacion["materno"],
            rfc=informacion["rfc"],
            curp=informacion["curp"],
            is_active=informacion["is_active"],
            correo=informacion["correo"],
            pfisica=informacion["pfisica"],
            token=token,
        )

        try:
            serializer = recipients_serializer.RecipientSerializer(
                data=recipient_openfin.__dict__
            )
            serializer.is_valid(raise_exception=True)

            message = """El destinatario fue actualizado exitosamente."""
            response_data = {
                "detail": message,
                "data": serializer.data,
            }
            # Solicita el panel de control del usuario a Open Fin usando el token
            self.get_user_dashboard(token)
            # Prepara el nombre del destinatario para el correo electrónico
            destinatario = f"{recipient_openfin.__dict__.get('nombre')} {recipient_openfin.__dict__.get('paterno')} {recipient_openfin.__dict__.get('materno')}"

            # Crea y envía el correo electrónico de notificación
            messages = messages_recipients.RecipientMessages()
            if serializer.data.get("is_active"):
                message_sent = messages.activate_recipient_message(self.username, self.user_email, destinatario)
            else:
                message_sent = messages.inactivate_recipient_message(self.username, self.user_email, destinatario)

            emailSender.send_email(self.user_email, message_sent.get("asunto"), message_sent.get("mensaje"), token)

            self.geolocation_service.save_geolocation(
                user=request.user,
                location=location,
                service=json.dumps({"Service": "Recipient", "Method": "update", "url": reverse("recipients")})
            )

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as error_exception:
            data = {
                "detail": "no se pudo dar actualizar el destinatario",
                "data": recipient_openfin,
            }
            print(error_exception)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Elimina un destinatario existente",
        operation_description="Se realiza la eliminacion de un destinatario en la cuenta",
        request_body=recipients_serializer.RecipientQueryParamSerializer(),
        responses={
            status.HTTP_200_OK: recipients_serializer.RecipientQueryParamSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
        tags=['Destinatarios']
    )
    def delete_recipient(self, request) -> Response:
        """Deactivate the recipient"""
        query_params_serializer = recipients_serializer.RecipientQueryParamSerializer(
            data=request.query_params
        )
        query_params_serializer.is_valid(raise_exception=True)
        iddestinatario = query_params_serializer.validated_data.get("iddestinatario")

        payload_serializer = GeolocationSerializer(data=request.data)
        print("geolocalizacion sin validar")
        payload_serializer.is_valid(raise_exception=True)

        print("geolocalizacion validada")
        latitude = float(payload_serializer.validated_data.get("latitude", 0) or 0)
        longitude = float(payload_serializer.validated_data.get("latitude", 0) or 0)
        location = Point(longitude, latitude)

        token = f"Bearer {request.user.open_fin_token}"

        recipient_openfin = recipients_engine.delete_recipient(
            iddestinatario=iddestinatario, token=token
        )
        if recipient_openfin["code"] == 200:
            data = {
                "detail": "Destinatario eliminado de forma exitosa",
                "data": recipient_openfin,
            }
            self.geolocation_service.save_geolocation(
                user=request.user,
                location=location,
                service=json.dumps({"Service":"Recipient","Method":"delete","url":reverse("recipients")})
            )
            return Response(data, status=status.HTTP_200_OK)

        elif recipient_openfin["code"] == 400:
            data = {
                "detail": "El destinatario tiene cuentas activas",
                "data": recipient_openfin,
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {
                "detail": "El destinatanrio no se pudo eliminar o no existe",
                "data": recipient_openfin,
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Lista todos los destinatarios",
        operation_description="Se realiza el alta de un destinatario en la cuenta",
        responses={
            status.HTTP_200_OK: recipients_serializer.RecipientSerializer(),
            status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        },
        tags=['Destinatarios']
    )
    def list_recipients(self, request) -> Response:
        """List recipients"""
        token = f"Bearer {request.user.open_fin_token}"
        print(f"OpenFin Token: \n {token}")
        query_param_serializer = recipients_serializer.RecipientQueryParamSerializer(
            data=request.data
        )
        query_param_serializer.is_valid(raise_exception=True)
        id_destinatario = request.query_params.get("iddestinatario")

        print(f"id destinatario {id_destinatario}")
        if id_destinatario is not None:
            try:
                destinatatio_openfin = recipients_engine.get_recipient(
                    iddestinatario=id_destinatario, token=token
                )
                print(f"data openfin:\n {destinatatio_openfin}")

                serializer = recipients_serializer.RecipientSerializer(
                    data=destinatatio_openfin.__dict__
                )

                print(
                    f"recipient serielized ==> {serializer.is_valid(raise_exception=False)}"
                )
                serializer.is_valid(raise_exception=True)

                response_data = {
                    "detail": "Consulta de destinatario exitosa",
                    "data": [serializer.data],
                }

                return Response(response_data, status=status.HTTP_200_OK)
            except Exception as error_exception:
                print(error_exception)
                response_data = {"detail": "beneficiario no encontrado", "data": ""}
                return Response(response_data, status=status.HTTP_403_FORBIDDEN)

        list_recipients = recipients_engine.list_recipient(token=token)
        serializer = recipients_serializer.RecipientSerializer(
            data=list_recipients, many=True
        )
        serializer.is_valid(raise_exception=True)
        response_data = {
            "detail": "Consulta de destinatarios exitosa",
            "data": serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def get_user_dashboard(self,token) -> Response:
        """List recipients"""

        try:
            user_dashboard_openfin = users_dashboard_engine.get_user_dashboard(
                 token=token
            )

            data=user_dashboard_openfin.__dict__
            self.username=data.get("nombre")
            self.user_email=data.get("correo")

        except Exception as error_exception:
            print(error_exception)
            response_data = {"detail": "Usuario no encontrado", "data": ""}
            return response_data

