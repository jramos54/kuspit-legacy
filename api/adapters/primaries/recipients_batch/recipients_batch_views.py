# Local utilities
import json, re
from django.conf import settings
import ast

import os
from drf_yasg import openapi
from rest_framework.decorators import api_view

from compartidos.serializers import NotFoundSerializer
from apps.backoffice.models import users as users_models
# Librerías de Terceros
from rest_framework.permissions import DjangoModelPermissions

from rest_framework.response import Response
from rest_framework import viewsets, status
from .tasks import upload_file_task
from . import recipients_batch_serializer
from uuid import uuid4
import redis

from ...secondaries.db_open_fin.repository_implementation_recipient_batch_openfin import \
    RecipientBatchImplementation
from .swagger_docs import (list_batch_recipients_docs,
                           apply_batch_recipients_docs,
                           delete_batch_recipient_file_docs,
                           get_recipient_batch_progress_docs,
                           list_uploaded_recipient_files_docs,
                           upload_recipient_batch_file_docs)

# Django REST Framework
from drf_yasg.utils import swagger_auto_schema

open_fin = RecipientBatchImplementation()
redis_url_0 = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
redis_client = redis.Redis.from_url(redis_url_0)

class FileUploadView(viewsets.GenericViewSet):
    """Views for CRUD Recipients"""

    serializer_class = recipients_batch_serializer.FilesImportedSerializer
    permission_classes = [DjangoModelPermissions]
    queryset = users_models.User.objects.all()

    @upload_recipient_batch_file_docs
    def upload_file(self, request) -> Response:
        """Upload recipients file"""
        token = f"Bearer {request.user.open_fin_token}"
        print(f"OpenFin Token: \n {token}")

        # Obtener el archivo del request
        file = request.FILES['file']
        task_id = str(uuid4())

        # Asegurarse de que el directorio de destino existe
        media_root = settings.MEDIA_ROOT
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
        upload_file_task.delay(task_id, file_path, token)

        return Response({"task_id": task_id}, status=202)

    @list_uploaded_recipient_files_docs
    def get_uploaded_files(self, request) -> Response:
        """List recipients"""
        token = f"Bearer {request.user.open_fin_token}"
        print(f"OpenFin Token: \n {token}")

        try:
            # Llama al servicio externo para obtener el dashboard del usuario
            openfin_response = open_fin.show_imports(
                token=token
            )
            print(openfin_response)
            # Serializa los datos obtenidos
            serializer = recipients_batch_serializer.FilesImportedSerializer(
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
            print(error_exception)
            response_data = {"detail": str(error_exception), "data": ""}
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)

    @list_batch_recipients_docs
    def get_file_details(self, request) -> Response:
        """List File details"""
        token = f"Bearer {request.user.open_fin_token}"

        id = request.query_params.get('id')
        try:
            # Llama al servicio externo para obtener el dashboard del usuario
            openfin_response = open_fin.detail_import(
                id=id,
                token=token
            )
            # print(f"VIEW - openfin response  {openfin_response}")
            # Serializa los datos obtenidos
            serializer = recipients_batch_serializer.DetailImportedSerielizer(
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

    @apply_batch_recipients_docs
    def apply_file_recipients(self, request) -> Response:
        """List recipients"""
        token = f"Bearer {request.user.open_fin_token}"
        print(f"OpenFin Token: \n {token}")

        id = request.query_params.get('id')

        try:
            # Llama al servicio externo para obtener el dashboard del usuario
            openfin_response = open_fin.apply_import(
                id=id,
                token=token
            )

            # Respuesta exitosa
            response_data = {
                "detail": "Se aplicaron las cargas masivas",
                "data": openfin_response,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as error_exception:
            print(error_exception)
            response_data = {"detail": str(error_exception), "data": ""}
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)

    @delete_batch_recipient_file_docs
    def delete_file_uploaded(self, request) -> Response:
        """List recipients"""
        token = f"Bearer {request.user.open_fin_token}"
        print(f"OpenFin Token: \n {token}")

        id = request.query_params.get('id')

        try:
            # Llama al servicio externo para obtener el dashboard del usuario
            openfin_response = open_fin.delete_import(
                id=id,
                token=token
            )

            # Respuesta exitosa
            response_data = {
                "detail": "Se elimino correctamente el archivo",
                "data": openfin_response,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as error_exception:
            print(error_exception)
            response_data = {"detail": str(error_exception), "data": ""}
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)


redis_url_1 = os.getenv('REDIS_URL_1', 'redis://redis:6379/1')
redis_client_1 = redis.Redis.from_url(redis_url_1)


def event_stream(task_id):
    print(f"Starting event stream for task_id: {task_id}")

    # Suscribirse al canal en Redis 0
    pubsub = redis_client.pubsub()
    pubsub.subscribe(f"file_status:{task_id}")
    print(f"Subscribed to file_status:{task_id}")

    for message in pubsub.listen():
        if message['type'] == 'message':
            try:
                # Decodificar el mensaje
                data = message['data'].decode('utf-8')
                print(f"Received message: {data}")

                # Enviar el mensaje al cliente en tiempo real
                yield f"data: {data}\n\n"

                # Comprobar si el mensaje contiene la cadena de finalización
                if "Proceso de carga a OpenFin terminado" in data:
                    print(f"Finalization message detected: {data}")

                    # Extraer la parte de "data:" del mensaje y convertirla en un diccionario de Python
                    data_part = data.split("data:", 1)[-1].strip() if 'data:' in data else ""

                    # Intentar convertir `data_part` a un diccionario de Python usando ast.literal_eval
                    try:
                        data_dict = ast.literal_eval(data_part)  # Convertir de forma segura
                        print(f"Data part successfully converted to dict: {data_dict}")
                    except (SyntaxError, ValueError) as e:
                        print(f"Failed to convert data part to dict: {e}")
                        data_dict = {}  # Usar un diccionario vacío como fallback

                    # Construir el JSON con el mensaje y los datos
                    final_message_json = {
                        "message": "Proceso de carga a OpenFin terminado",
                        "data": data_dict
                    }

                    try:
                        # Almacenar el mensaje final como JSON en Redis en la base de datos 1
                        redis_client_1.set(f"myapp:final_message:{task_id}", json.dumps(final_message_json))
                        print(f"Final message stored in Redis 1 for task {task_id}")
                    except Exception as e:
                        print(f"Failed to store final message in Redis 1: {e}")

                    # Enviar la respuesta final formateada al cliente
                    yield f"data: {json.dumps(final_message_json)}\n\n"

                    # Salir del bucle y cerrar el flujo
                    break
            except Exception as e:
                print(f"Error processing message: {e}")

@get_recipient_batch_progress_docs
@api_view(['GET'])
def file_progress_updates(request, task_id):
    print(f"Checking final message and errors in Redis for task_id: {task_id}")

    try:
        # Recupera los errores de Redis
        errors_data = redis_client_1.get(f"myapp:errors:{task_id}")

        # Si hay errores, decodifícalos y devuelve inmediatamente
        if errors_data:
            errors_data = json.loads(errors_data.decode('utf-8'))
            print(f"Errores recuperados: {errors_data}")
            return Response(errors_data, status=status.HTTP_200_OK)

        # Si no hay errores, intenta recuperar el mensaje final
        final_message = redis_client_1.get(f"myapp:final_message:{task_id}")
        if final_message:
            final_message_str = final_message.decode('utf-8')
            data_index = final_message_str.find('data:')
            if data_index != -1:
                data_part = final_message_str[data_index + len('data:'):].strip()
                data_part = data_part.replace("'", '"')
                data_part = re.sub(r'\bFalse\b', 'false', data_part)
                data_part = re.sub(r'\bNone\b', 'null', data_part)

                final_message_json = {
                    "message": "Proceso de carga a OpenFin terminado",
                    "data": json.loads(data_part),
                    "errores": []
                }
                return Response(final_message_json, status=status.HTTP_200_OK)
            else:
                print("Data part not found in the final message.")
                return Response({"error": "Data part not found in final message."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            print("Final message not found in Redis.")
            return Response({"error": "Final message not found or is empty."}, status=status.HTTP_404_NOT_FOUND)

    except json.JSONDecodeError as e:
        print(f"JSON decoding failed: {e}")
        return Response({"error": "Invalid JSON format in final message."},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        print(f"Failed to retrieve data from Redis: {e}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

