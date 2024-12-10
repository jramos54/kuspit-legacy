# Local utilities
import json, re
from django.conf import settings
import ast
from django.urls import reverse
from django.contrib.gis.geos import Point
from uuid import uuid4
import redis

import os
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi

from apps.backoffice.models import users as users_models
# Librerías de Terceros
from rest_framework.permissions import DjangoModelPermissions

from rest_framework.response import Response
from rest_framework import viewsets, status
from .tasks import upload_file_task
from . import payments_batch_serializer
from ....adapters.secondaries.Geolocation.geolocation_service import GeolocationService
from ....adapters.secondaries.Geolocation.geolocation_serializer import GeolocationSerializer

from django.http import StreamingHttpResponse

from ...secondaries.db_open_fin.repository_implementation_payments_batch_openfin import \
    PaymentsBatchImplementation

from .swagger_docs import (list_batch_payment_details_docs,
                           list_uploaded_files_docs,
                           apply_batch_payment_docs,
                           get_batch_progress_docs,
                           upload_batch_payment_file_docs
                           )

open_fin = PaymentsBatchImplementation()
redis_url_0 = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
redis_client = redis.Redis.from_url(redis_url_0)


class FilePaymentsUploadView(viewsets.GenericViewSet):
    """Views for CRUD Recipients"""

    serializer_class = payments_batch_serializer.PaymentFilesImportedSerializer
    permission_classes = [DjangoModelPermissions]
    queryset = users_models.User.objects.all()
    geolocation_service = GeolocationService()

    @upload_batch_payment_file_docs
    def upload_file(self, request) -> Response:
        """Upload recipients file"""
        token = f"Bearer {request.user.open_fin_token}"
        print(f"OpenFin Token: \n {token}")

        data_serialized = payments_batch_serializer.PaymentFileUploadGeolocation(data=request.data)
        data_serialized.is_valid(raise_exception=True)

        # Obtener el archivo del request
        file = data_serialized.validated_data['file_upload']['file']
        kauxiliar = data_serialized.validated_data['file_upload']['kauxiliar']
        geolocalization_data = data_serialized.validated_data.get("geolocalizacion", {})

        latitude = float(geolocalization_data.get("latitude", 0))
        longitude = float(geolocalization_data.get("longitude", 0))
        location = Point(longitude, latitude)

        # Asegurarse de que el directorio de destino existe
        media_root = settings.MEDIA_ROOT
        task_id = str(uuid4())

        if not os.path.exists(media_root):
            os.makedirs(media_root)  # Crea el directorio si no existe

        # Guardar el archivo temporalmente en el sistema de archivos
        file_path = os.path.join(media_root, f'temp_{task_id}_{file.name}')
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        # Publicar un mensaje en Redis indicando que la carga ha comenzado
        redis_client.publish(f"file_status:{task_id}", "File received and upload started")

        # Iniciar la tarea en segundo plano, pasando la ruta del archivo
        upload_file_task.delay(task_id, file_path,kauxiliar, token)

        self.geolocation_service.save_geolocation(
            user=request.user,
            location=location,
            service=json.dumps({"Service": "Payment Batch", "Method": "post", "url": reverse("payment-upload-file")})
        )

        return Response({"task_id": task_id}, status=202)

    @list_uploaded_files_docs
    def get_uploaded_files(self, request) -> Response:
        """List recipients"""
        token = f"Bearer {request.user.open_fin_token}"
        print(f"OpenFin Token: \n {token}")
        kauxiliar=request.query_params.get('kauxiliar')

        try:
            # Llama al servicio externo para obtener el dashboard del usuario
            openfin_response = open_fin.show_imports(kauxiliar=kauxiliar,token=token)
            # Serializa los datos obtenidos
            serializer = payments_batch_serializer.PaymentFilesImportedSerializer(
                data=openfin_response,many=True
            )

                    # Valida los datos serializados
            serializer.is_valid(raise_exception=True)

            # Respuesta exitosa
            response_data = {
                "detail": "Consulta de Archivos exitosa",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as error_exception:
            response_data = {"detail": str(error_exception), "data": ""}
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)

    @list_batch_payment_details_docs
    def get_file_details(self, request) -> Response:
        """List recipients"""
        token = f"Bearer {request.user.open_fin_token}"
        print(f"OpenFin Token: \n {token}")

        id = request.query_params.get('idarchivo')
        try:
            # Llama al servicio externo para obtener el dashboard del usuario
            openfin_response = open_fin.detail_import(
                id=id,
                token=token
            )
            # Serializa los datos obtenidos
            serializer = payments_batch_serializer.PaymentDetailImportedSerielizer(
                data=openfin_response, many=True
            )

            # Valida los datos serializados
            serializer.is_valid(raise_exception=True)

            # Respuesta exitosa
            response_data = {
                "detail": "Consulta del contenido del archivo exitosa",
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as error_exception:
            print(error_exception)
            response_data = {"detail": str(error_exception), "data": ""}
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)

    @apply_batch_payment_docs
    def apply_file_recipients(self, request) -> Response:
        """List recipients"""
        token = f"Bearer {request.user.open_fin_token}"
        print(f"OpenFin Token: \n {token}")

        id = request.query_params.get('idarchivo')

        try:
            # Llama al servicio externo para obtener el dashboard del usuario
            openfin_response = open_fin.apply_import(
                id=id,
                token=token
            )
            if openfin_response.get('status'):
            # Respuesta exitosa
                response_data = {
                    "detail": "Se aplicaron las cargas masivas",
                    "data": openfin_response,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "detail": "Error al aplicar las cargas masivas",
                    "data": openfin_response,
                }
                return Response(response_data, status=status.HTTP_403_FORBIDDEN)

        except Exception as error_exception:
            print(error_exception)
            response_data = {"detail": str(error_exception), "data": ""}
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)


redis_url_1 = os.getenv('REDIS_URL_1', 'redis://redis:6379/1')
redis_client_1 = redis.Redis.from_url(redis_url_1)


def event_stream(task_id):

    # Suscribirse al canal en Redis 0
    pubsub = redis_client.pubsub()
    pubsub.subscribe(f"file_status:{task_id}")

    for message in pubsub.listen():
        if message['type'] == 'message':
            try:
                # Decodificar el mensaje
                data = message['data'].decode('utf-8')
                # Enviar el mensaje al cliente en tiempo real
                yield f"data: {data}\n\n"

                # Comprobar si el mensaje contiene la cadena de finalización
                if "Proceso de carga a OpenFin terminado" in data:

                    # Extraer la parte de "data:" del mensaje y convertirla en un diccionario de Python
                    data_part = data.split("data:", 1)[-1].strip() if 'data:' in data else ""

                    # Intentar convertir `data_part` a un diccionario de Python usando ast.literal_eval
                    try:
                        data_dict = ast.literal_eval(data_part)  # Convertir de forma segura
                    except (SyntaxError, ValueError) as e:
                        data_dict = {}  # Usar un diccionario vacío como fallback

                    # Construir el JSON con el mensaje y los datos
                    final_message_json = {
                        "message": "Proceso de carga a OpenFin terminado",
                        "data": data_dict
                    }

                    try:
                        # Almacenar el mensaje final como JSON en Redis en la base de datos 1
                        redis_client_1.set(f"myapp:final_message:{task_id}", json.dumps(final_message_json))
                    except Exception as e:
                        print(f"Failed to store final message in Redis 1: {e}")

                    # Enviar la respuesta final formateada al cliente
                    yield f"data: {json.dumps(final_message_json)}\n\n"

                    # Salir del bucle y cerrar el flujo
                    break
            except Exception as e:
                print(f"Error processing message: {e}")

@get_batch_progress_docs
@api_view(['GET'])
def file_progress_updates(request, task_id):
    print(f"Checking final message in Redis for task_id: {task_id}")

    # Verificar si ya se ha almacenado el mensaje final en Redis en la base de datos 1
    try:
        final_message = redis_client_1.get(f"myapp:final_message:{task_id}")
        if final_message:
            print(f"Final message found in Redis for task_id: {task_id}")
            print(f"Raw final message: {final_message}")
        else:
            print(f"No final message found in Redis for task_id: {task_id}")
    except Exception as e:
        print(f"Failed to retrieve final message from Redis: {e}")
        final_message = None

    if final_message:
        try:
            # Decodificar el mensaje de bytes a string
            final_message_str = final_message.decode('utf-8')
            print(f"Decoded final message: {final_message_str}")

            # Extraer la parte de la cadena que contiene 'data:'
            data_index = final_message_str.find('data:')
            if data_index != -1:
                data_part = final_message_str[data_index + len('data:'):].strip()
                print(f"Extracted data part: {data_part}")

                # Reemplazar comillas simples por comillas dobles
                data_part = data_part.replace("'", '"')
                # Convertir False a false para JSON
                data_part = re.sub(r'\bFalse\b', 'false', data_part)
                # Convertir None a null para JSON
                data_part = re.sub(r'\bNone\b', 'null', data_part)
                print(f"Sanitized data part for JSON: {data_part}")

                # Construir el JSON con el mensaje y los datos
                final_message_json = {
                    "message": "Proceso de carga a OpenFin terminado",
                    "data": json.loads(data_part)
                }
                return Response(final_message_json, status=status.HTTP_200_OK)
            else:
                print("No data part found in the message.")
                return Response({"error": "Data part not found in final message."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except json.JSONDecodeError as e:
            print(f"JSON decoding failed: {e}")
            return Response({"error": "Invalid JSON format in final message."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        # Si final_message es None o vacío, devolver un error
        return Response({"error": "Final message not found or is empty."}, status=status.HTTP_404_NOT_FOUND)

    # Si no hay mensaje final, iniciar el flujo de eventos en tiempo real
    print(f"No final message, starting event stream for task_id: {task_id}")
    response = StreamingHttpResponse(event_stream(task_id), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response