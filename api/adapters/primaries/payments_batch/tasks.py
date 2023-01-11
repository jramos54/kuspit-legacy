from celery import shared_task
from redis import Redis
import redis

import time
import os
import csv
from ...secondaries.db_open_fin.repository_implementation_payments_batch_openfin import PaymentsBatchImplementation

# Configuración del cliente Redis
redis_url_0 = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
redis_client = redis.Redis.from_url(redis_url_0)

@shared_task()
def upload_file_task(task_id, file_path,kauxiliar, token):
    try:
        # Comenzar la tarea y enviar una señal de inicio
        redis_client.publish(f"file_status:{task_id}", "Iniciando la carga del archivo.")
        print(f"Iniciando la carga del archivo: {file_path}")

        # Verificar que el archivo exista
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo {file_path} no fue encontrado.")

        # Obtener el tamaño total del archivo
        total_size = os.path.getsize(file_path)
        processed_size = 0

        # Leer el contenido del archivo y realizar operaciones necesarias
        with open(file_path, 'rb') as f:
            chunk_size = 1024 * 1024  # Leer en fragmentos de 1MB
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break

                # Actualizar el tamaño procesado
                processed_size += len(chunk)

                # Calcular el progreso como un porcentaje
                progress = int((processed_size / total_size) * 100)
                redis_client.publish(f"file_status:{task_id}", f"Progreso de la carga: {progress}%")
                print(f"Progreso de la carga: {progress}%")

        # Publicar la finalización de la carga
        redis_client.publish(f"file_status:{task_id}", "Carga completada. Se inicia la validación.")
        print("Carga completada. Se inicia la validación.")

        # Iniciar la validación del archivo después de la carga
        validate_file_task.delay(task_id, file_path, kauxiliar,token)
        print(f"Tarea de validación iniciada para task_id: {task_id}")
        return {'status': 'success', 'message': 'Archivo cargado y procesado exitosamente.'}


    except Exception as e:
        redis_client.publish(f"file_status:{task_id}", f"Error al procesar el archivo: {str(e)}")
        print(f"Error al procesar el archivo: {str(e)}")

@shared_task
def validate_file_task(task_id, file_path, kauxiliar, token):
    print(f"Tarea de validación iniciada para task_id: {task_id}")

    result = []
    # Inicializar la primera lista vacía para los encabezados
    result.append([])

    # Lista para guardar las líneas incorrectas junto con sus errores
    invalid_lines = []

    # Lista para almacenar las líneas transformadas
    transformed_lines = []

    try:
        redis_client.publish(f"file_status:{task_id}", "Leyendo y procesando el archivo.")
        print(f"Leyendo y procesando el archivo: {file_path}")

        # Obtener solo el nombre del archivo (por ejemplo, "nombrearchivo.csv") de la ruta completa
        file_name = os.path.basename(file_path)

        # Abrir el archivo CSV con soporte para diferentes delimitadores
        with open(file_path, 'r') as file:
            # Detectar el delimitador automáticamente
            try:
                dialect = csv.Sniffer().sniff(file.read(1024))
                file.seek(0)
            except csv.Error:
                redis_client.publish(f"file_status:{task_id}", "No se pudo detectar el delimitador del archivo CSV.")
                print("Error: No se pudo detectar el delimitador del archivo CSV.")
                return {
                    'detail': "Error: No se pudo detectar el delimitador del archivo CSV.",
                }
            file.seek(0)
            reader = csv.reader(file, delimiter=dialect.delimiter)
            # next(reader, None)
            # Iterar sobre las filas del archivo CSV
            for row in reader:
                if reader.line_num == 1:
                    # Saltar la primera fila si es el encabezado
                    continue
                print(row)
                # Validación y transformación de datos
                try:
                    (
                         codigo_institucion, importe,destinatario,
                        tipo_cuenta, cuenta, concepto,
                        referencia
                    ) = row
                except ValueError:
                    error_message = f"Error de formato en la línea {reader.line_num}: número incorrecto de columnas."
                    invalid_lines.append({'row': row, 'errors': error_message})
                    redis_client.publish(f"file_status:{task_id}", error_message)
                    print(error_message)
                    continue

                # Transformar la fila según las reglas y agregar a la lista transformada
                transformed_row = [
                    codigo_institucion,
                    importe,
                    destinatario,
                    tipo_cuenta,
                    cuenta,
                    concepto,
                    referencia,
                ]
                transformed_lines.append(transformed_row)

        transformed_lines.insert(0,[])
        print(f"Lineas transformadas: {transformed_lines}")

        # Si todas las líneas son válidas, iniciar la tarea openfin_upload_task
        redis_client.publish(f"file_status:{task_id}", "Validación correcta, comienza la carga.")
        print("Validación correcta, comienza la carga.")
        openfin_upload_task.delay(task_id, file_name, transformed_lines, kauxiliar,token)

    except Exception as e:
        redis_client.publish(f"file_status:{task_id}", f"Error en la validación: {str(e)}")
        print(f"Error en la validación: {str(e)}")
        return {
            'detail': "Error en la validación",
            'error': str(e)
        }

    finally:
        # Eliminar el archivo temporal después de que se complete el procesamiento
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Archivo temporal eliminado: {file_path}")

    return {
        'detail': "La validación de los datos se realizó correctamente."
    }

redis_url_1 = os.getenv('REDIS_URL_1', 'redis://redis:6379/1')
redis_client_1 = redis.Redis.from_url(redis_url_1)

@shared_task
def openfin_upload_task(task_id, file_name, payments_data,kauxiliar, token):
    try:
        redis_client.publish(f"file_status:{task_id}", "Iniciando carga a OpenFin.")
        print("Iniciando carga a OpenFin.")

        open_fin = PaymentsBatchImplementation()
        openfin_response = open_fin.import_payments(filename=file_name, payments=payments_data, kauxiliar=kauxiliar,token=token)
        print(f"OPENFIN - {openfin_response}")
        if openfin_response.get('status'):
            openfin_id = open_fin.get_imports(filename=file_name,kauxiliar=kauxiliar, token=token)
            if openfin_id:
                final_message = f"Proceso de carga a OpenFin terminado, data:{openfin_id}"
                redis_client.publish(f"file_status:{task_id}", final_message)
                print(f"La carga se realizó con éxito: {openfin_id}")
            else:
                final_message = "Proceso de carga a OpenFin terminado,data:{detail:La carga falló.}"
                redis_client.publish(f"file_status:{task_id}", final_message)
                print("La carga falló.")
        else:
            final_message = "Proceso de carga a OpenFin terminado, data:{detail:La carga falló.}"
            redis_client.publish(f"file_status:{task_id}", final_message)
            print("La carga falló.")

        # Guardar el estado final en Redis 1
        try:
            redis_client_1.set(f"myapp:final_message:{task_id}", final_message)
            print(f"Final message stored in Redis 1 for task {task_id}")
        except Exception as e:
            print(f"Failed to store final message in Redis 1: {e}")

        print("Carga completada.")

    except Exception as e:
        error_message = f"Error durante la carga: {str(e)}"
        redis_client.publish(f"file_status:{task_id}", error_message)
        print(error_message)

        # Guardar el mensaje de error en Redis 1
        try:
            redis_client_1.set(f"myapp:final_message:{task_id}", error_message)
            print(f"Error message stored in Redis 1 for task {task_id}")
        except Exception as e:
            print(f"Failed to store error message in Redis 1: {e}")