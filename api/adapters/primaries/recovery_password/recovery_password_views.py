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
from ....adapters.secondaries.factory.constructor_password_recovery import (
    constructor_user_dashboard as recovery_password,
)
from apps.backoffice.models import User
from apps.backoffice.models import Log2FA

from ....engine.domain.exceptions import exceptions_recipient
from ....engine.domain.messages import messages_recovery_password

from . import recovery_password_serializer
from .swagger_docs import (validate_temp_code_docs,
                           create_new_password_docs,
                           generate_temp_token_docs,
                           get_security_questions_docs,
                           submit_security_answers_docs)

from ....adapters.secondaries.factory.constructor_email import constructor_user_dashboard as email_sender

emailSender=email_sender()
recoveryPassword=recovery_password()


class RecoveryPasswordViewSet(viewsets.GenericViewSet):
    """Vista para operaciones CRUD en Recipients"""

    # Define la clase serializer a utilizar
    serializer_class = recovery_password_serializer.RecoveryTokenEmailSerializer
    # permission_classes = [DjangoModelPermissions]
    queryset = users_models.User.objects.all()

    def __init__(self):
        # Inicializa las variables de instancia para el nombre de usuario y el correo electrónico
        self.username = None
        self.user_email = None

    @generate_temp_token_docs
    def generate_token(self, request) -> Response:
        """Crear un nuevo destinatario"""

        data = request.data  # Obtiene los datos de la solicitud

        # Deserializa los datos
        data_serialized = recovery_password_serializer.RecoveryTokenEmailSerializer(data=data)
        try:
            data_serialized.is_valid(raise_exception=True)  # Valida los datos
            informacion = data_serialized.data  # Extrae los datos validados

        except Exception as error_exception:
            # Maneja la excepción de CURP inválido
            return Response(error_exception.message, status=status.HTTP_400_BAD_REQUEST)

        self.get_user_dashboard(informacion.get('email'))
        self.user_email = informacion.get('email')

        try:

            temp_token_openfin = recoveryPassword.create_token_temp(
                email=informacion.get('email')
            )
            relative_url = "http://10.20.100.4:80/autenticacion/reestablecer-credenciales"
            #relative_url = reverse('preguntas')
            new_url=request.build_absolute_uri(f'{relative_url}?token={temp_token_openfin.get("token")}&email={self.user_email}')
            temp_token_openfin["link"]=new_url

        except KeyError as error_exception:
            error_type = error_exception.args[0]
            message = {
                "detail": f"No se genero el token {error_type}"
            }
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer = recovery_password_serializer.RecoveryTokenSerializer(
                data=temp_token_openfin
            )
            serializer.is_valid(raise_exception=True)  # Valida los datos serializados

            # Prepara el mensaje de respuesta de éxito
            message = "Se genero el token temporal"
            response_data = {
                "detail": message,
                "data": serializer.data,
            }

            # Crea y envía el correo electrónico de notificación
            messages = messages_recovery_password.RecoveryPasswordMessages()
            message_sent = messages.forgot_password_message(self.username,new_url)
            token=''
            emailSender.send_email(self.user_email, message_sent.get("asunto"), message_sent.get("mensaje"),token)

            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as error_exception:

            data = {
                "detail": "No se pudo generar el token temporal",
                "data": [],
            }
            print(error_exception)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @get_security_questions_docs
    def get_questions(self, request) -> Response:
        """Crear un nuevo destinatario"""

        try:
            # Obtener el token desde los parámetros de la URL (query params)
            temp_token = request.query_params.get('token')
            if not temp_token:
                raise KeyError('token')

            questions_openfin = recoveryPassword.get_questions(
                temp_token=temp_token
            )
            print(f"Preguntas de open fin {questions_openfin}")

        except KeyError as error_exception:
            error_type = error_exception.args[0]
            message = {
                "detail": f"No se pudieron generar las preguntas: {error_type}"
            }
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer = recovery_password_serializer.RecoveryQuestionsSerializer(
                data=questions_openfin.get('preguntas'), many=True
            )
            serializer.is_valid(raise_exception=True)  # Valida los datos serializados

            # Prepara el mensaje de respuesta de éxito
            message = "preguntas obtenidas"
            response_data = {
                "detail": message,
                "data": serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as error_exception:

            data = {
                "detail": "Error al generar las preguntas",
                "data": [],
            }
            print(error_exception)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @submit_security_answers_docs
    def send_answers(self, request) -> Response:
        """Crear un nuevo destinatario"""

        try:
            # Obtener el token desde los parámetros de la URL (query params)
            temp_token = request.query_params.get('token')
            self.user_email = request.query_params.get('email')
            self.get_user_dashboard(self.user_email)

            if not temp_token:
                raise KeyError('token')

            respuestas = request.data
            questions_openfin = recoveryPassword.validate_questions(
                temp_token=temp_token, anwsers=respuestas
            )

            user = User.objects.get(email=self.user_email)
            log_2fa, created = Log2FA.objects.get_or_create(user=user)

            # Lógica de bloqueo si hay 3 intentos fallidos de responder preguntas
            if log_2fa.questions_attempt >= 3:
                return Response({"detail": "Cuenta bloqueada por múltiples intentos fallidos."},
                                status=status.HTTP_403_FORBIDDEN)
            print(f"VIEW code -- {questions_openfin.get('code') }")
            if questions_openfin.get('code') == 0:
                # Respuestas correctas, reiniciar el conteo de intentos
                log_2fa.questions_attempt = 0
                log_2fa.save()

                message = "Respuestas correctas"
                response_data = {
                    "detail": message,
                    "data": [],
                }

                # Genera el código provisional
                recovery_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])

                log_2fa.temp_code = recovery_code
                log_2fa.save()

                # Crea y envía el correo electrónico de notificación
                messages = messages_recovery_password.RecoveryPasswordMessages()
                message_sent = messages.recovery_code(self.username, recovery_code)
                token = ''
                emailSender.send_email(self.user_email, message_sent.get("asunto"), message_sent.get("mensaje"), token)

                return Response(response_data, status=status.HTTP_200_OK)

            else:
                # Respuestas incorrectas, incrementar intentos
                log_2fa.questions_attempt += 1
                log_2fa.save()

                error_message = questions_openfin.get('message', 'Respuestas incorrectas')
                response_data = {
                    "detail": error_message,
                    "next_step": "Generar un nuevo token",
                    "redirect_url": reverse('temp-token')
                }

                # Redirigir al endpoint para generar un nuevo token
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        except KeyError as error_exception:
            error_type = error_exception.args[0]
            message = {
                "detail": f"No se pudieron generar las preguntas: {error_type}"
            }
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    @create_new_password_docs
    def new_password(self, request) -> Response:
        """Cambiar la contraseña del usuario"""

        print(f"Datos recibidos en request data: {request.data}")

        serializer= recovery_password_serializer.RecoveryPasswordEmailSerializer(data=request.data)
        print(f"Datos recibidos en initial data: {serializer.initial_data}")

        try:
            if 'new_password' not in request.data:
                print("El campo 'password' no está presente en la solicitud antes de la validación.")

            serializer.is_valid(raise_exception=True)
            print(f"Datos validados: {serializer.validated_data}")

        except serializers.ValidationError as error_exception:
            return Response({"detail": error_exception.detail}, status=status.HTTP_400_BAD_REQUEST)

        temp_token = request.query_params.get('token')
        if not temp_token:
            return Response({"detail": "Falta el token en la solicitud."}, status=status.HTTP_400_BAD_REQUEST)

        datos = serializer.validated_data
        print(f"Datos después de la validación: {datos}")
        print(f"email {datos.get('email')} password {datos.get('new_password')}")
        cambio_password_openfin = recoveryPassword.change_password(
            temp_token=temp_token, email=datos.get("email"), password=datos.get("new_password")
        )

        # Verifica la respuesta del sistema externo
        if cambio_password_openfin.get('code', 0) == 200:
            # Obtener el usuario y cambiar la contraseña localmente
            try:
                user = User.objects.get(email=datos.get("email"))
                hashed_password = make_password(datos.get("new_password"), hasher="pbkdf2_sha256")
                user.password = hashed_password
                user.save()  # Guardar los cambios en la base de datos

                message = "Password cambiado exitosamente"
                return Response({"detail": message}, status=status.HTTP_200_OK)

            except User.DoesNotExist:
                return Response({"detail": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "No se pudo cambiar la contraseña en OpenFin."}, status=status.HTTP_400_BAD_REQUEST)

    @validate_temp_code_docs
    def validate_code(self, request) -> Response:
        """Validar el código temporal"""

        try:
            # Obtener el token desde los parámetros de la URL (query params)
            temp_token = request.query_params.get('token')
            self.user_email = request.query_params.get('email')
            self.get_user_dashboard(self.user_email)

            if not temp_token:
                raise KeyError('token')

            codigo = request.data

            user = User.objects.get(email=self.user_email)
            log_2fa = Log2FA.objects.get(user=user)

            # Si hay 3 intentos fallidos, bloquear la cuenta
            if log_2fa.failed_attempts >= 3:
                return Response({"detail": "Cuenta bloqueada por múltiples intentos fallidos."},
                                status=status.HTTP_403_FORBIDDEN)

            # Verificar si el código es correcto
            if log_2fa.temp_code == codigo.get('codigo'):
                log_2fa.failed_attempts = 0  # Resetear los intentos fallidos en caso de éxito
                user.login_attempts = 0 # Desbloquea los logins fallidos
                user.save()
                log_2fa.save()

                message = "Código Correcto"
                response_data = {
                    "detail": message,
                    "data": [],
                }

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                # Incrementar los intentos fallidos si el código es incorrecto
                log_2fa.failed_attempts += 1
                log_2fa.save()

                message = "Código incorrecto"
                response_data = {
                    "detail": message,
                    "data": [],
                }


                # Generar un nuevo código si el usuario falla
                recovery_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
                log_2fa.temp_code = recovery_code
                log_2fa.save()

                # Crea y envía el correo electrónico de notificación
                messages = messages_recovery_password.RecoveryPasswordMessages()
                message_sent = messages.recovery_code(self.username, recovery_code)
                token = ''
                emailSender.send_email(self.user_email, message_sent.get("asunto"), message_sent.get("mensaje"), token)

                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        except KeyError as error_exception:
            error_type = error_exception.args[0]
            message = {
                "detail": f"Error al validar el código: {error_type}"
            }
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def get_user_dashboard(self, email):
        """List recipients"""
        user = get_object_or_404(users_models.User, email=email)
        self.username=user.username

