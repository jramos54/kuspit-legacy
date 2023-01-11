from celery import shared_task
from redis import Redis
import redis
import json
import time
import os
import csv
from ...secondaries.db_open_fin.repository_implementation_recipient_batch_openfin import RecipientBatchImplementation
from datetime import datetime

# Configuración del cliente Redis
redis_url_0 = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0')
redis_client = redis.Redis.from_url(redis_url_0)


redis_url_1 = os.getenv('REDIS_URL_1', 'redis://redis:6379/1')
redis_client_1 = redis.Redis.from_url(redis_url_1)

@shared_task()
def upload_file_task(task_id, file_path, token):
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
        validate_file_task.delay(task_id, file_path, token)
        print(f"Tarea de validación iniciada para task_id: {task_id}")
        return {'status': 'success', 'message': 'Archivo cargado y procesado exitosamente.'}


    except Exception as e:
        redis_client.publish(f"file_status:{task_id}", f"Error al procesar el archivo: {str(e)}")
        print(f"Error al procesar el archivo: {str(e)}")


@shared_task
def validate_file_task(task_id, file_path, token):
    print(f"Tarea de validación iniciada para task_id: {task_id}")

    alias_set = set()
    cuenta_set = set()
    cuenta_reg_set=set()
    invalid_lines = []  # Lista que acumula los errores
    valid_lines=[]
    transformed_lines = []

    try:
        redis_client.publish(f"file_status:{task_id}", "Leyendo y procesando el archivo.")
        file_name = os.path.basename(file_path)

        with open(file_path, 'r') as file:
            # Intentar detectar el delimitador automáticamente
            try:
                sample = file.read(1024)
                dialect = csv.Sniffer().sniff(sample)
                file.seek(0)
                delimiter = dialect.delimiter
            except csv.Error:
                delimiter = ','  # Usa un delimitador predeterminado si no se detecta automáticamente

            file.seek(0)
            reader = csv.reader(file, delimiter=delimiter)

            for row in reader:
                if reader.line_num == 1:
                    continue  # Omite el encabezado

                # Validación de la fila
                try:
                    (
                        cuenta, alias, destinatarios, codigo_institucion,
                        tipo_cuenta, cuenta_val, limite_operacion,
                        num_operaciones, rfc, email, tipo_persona
                    ) = row
                except ValueError:
                    error_message = f"Error de formato en la línea {reader.line_num}: número incorrecto de columnas."
                    invalid_lines.append({
                        'linea': reader.line_num,
                        'contenido': row,  # Incluye el contenido de la fila en el error
                        'error': error_message
                    })
                    redis_client.publish(f"file_status:{task_id}", error_message)
                    continue

                # Se convierte el valor CLABE a numerico 40
                if tipo_cuenta == "CLABE":
                    tipo_cuenta=40
                # Reglas de validación
                errors = {}

                if tipo_cuenta == "CLABE":
                    tipo_cuenta=40
                    
                if alias in alias_set:
                    errors["alias"]={"value":alias,"isError":True,"messageError":"Alias duplicado"}
                else:
                    alias_set.add(alias)

                if cuenta_val in cuenta_set:
                    errors["cuenta_beneficiario"]={"value":cuenta_val,"isError":True,"messageError":"Se encontró cuenta duplicada"}
                else:
                    cuenta_set.add(cuenta_val)

                if len(cuenta_val) != 18:
                    errors["cuenta_beneficiario"]={"value":cuenta_val,"isError":True,"messageError":"La cuenta debe ser de 18 dígitos"}

                if cuenta_val[:3] != codigo_institucion[-3:]:
                    errors["institucion"]={"value":codigo_institucion,"isError":True,"messageError":"Cuenta y código de institución no coinciden"}

                if tipo_persona=="FISICA" and len(rfc)!=13:
                    errors["rfc"]={"value":rfc,"isError":True,"messageError":"Longitud de RFC no coincide"}

                if tipo_persona=="MORAL" and len(rfc)!=12:
                    errors["rfc"]={"value":rfc,"isError":True,"messageError":"Longitud de RFC no coincide"}

                if cuenta in cuenta_reg_set:
                    errors["idregistro"]={"value":cuenta,"isError":True,"messageError":"id de registro duplicado"}
                else:
                    alias_set.add(alias)

                if errors:
                    error_message = ", ".join(errors)
                    invalid_lines.append({
                        'linea': reader.line_num,
                        'contenido': {#row,  # Incluye el contenido de la fila en el error
                            "idarchivo": None,
                            "idregistro":errors.get("idregistro",cuenta),
                            "nombre": destinatarios,
                            "tipo_persona": tipo_persona,
                            "rfc": errors.get("rfc",rfc),
                            "alias": errors.get("alias",alias),
                            "institucion": errors.get("institucion",codigo_institucion),
                            "tipo_cuenta_beneficiario": tipo_cuenta,
                            "cuenta_beneficiario": errors.get("cuenta_beneficiario",cuenta_val),
                            "limite_operacion": limite_operacion,
                            "numero_operaciones": num_operaciones,
                            "email": email,
                            "fecha_real": datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3] + " CST",
                            "idbeneficiario": None,
                            "msg": None
                        },
                    })
                    redis_client.publish(f"file_status:{task_id}", error_message)
                else:
                    valid_lines.append({
                        'linea': reader.line_num,
                        'contenido': {  # row,  # Incluye el contenido de la fila en el error
                            "idarchivo": None,
                            "idregistro": cuenta,
                            "nombre": destinatarios,
                            "tipo_persona": tipo_persona,
                            "rfc": rfc,
                            "alias": alias,
                            "institucion": codigo_institucion,
                            "tipo_cuenta_beneficiario": tipo_cuenta,
                            "cuenta_beneficiario": cuenta_val,
                            "limite_operacion": limite_operacion,
                            "numero_operaciones": num_operaciones,
                            "email": email,
                            "fecha_real": datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3] + " CST",
                            "idbeneficiario": None,
                            "msg": None
                        },
                    })

                transformed_row = [
                    None,
                    alias,
                    destinatarios,
                    codigo_institucion,
                    tipo_cuenta,
                    cuenta_val,
                    limite_operacion,
                    num_operaciones,
                    rfc,
                    email,
                    tipo_persona
                ]
                transformed_lines.append(transformed_row)

        # Almacenar errores en Redis si los hay y finalizar
        if invalid_lines:
            error_data = {
                "detail": "Existen errores en el archivo",
                "file_content": invalid_lines + valid_lines
            }
            # Guarda los errores en Redis con el contenido completo de cada fila
            redis_client_1.set(f"myapp:errors:{task_id}", json.dumps(error_data))
            return error_data

        # Si no hay errores, continuar con la carga a OpenFin
        redis_client.publish(f"file_status:{task_id}", "Validación correcta, comienza la carga.")
        openfin_upload_task.delay(task_id, file_name, transformed_lines, token)

    except Exception as e:
        redis_client.publish(f"file_status:{task_id}", f"Error en la validación: {str(e)}")
        print(f"Error en la validación: {str(e)}")
        return {'detail': "Error en la validación", 'error': str(e)}

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Archivo temporal eliminado: {file_path}")

@shared_task
def openfin_upload_task(task_id, file_name, recipients_data, token):
    try:
        redis_client.publish(f"file_status:{task_id}", "Iniciando carga a OpenFin.")
        print("Iniciando carga a OpenFin.")

        open_fin = RecipientBatchImplementation()
        openfin_response = open_fin.import_recipients(filename=file_name, recipients=recipients_data, token=token)

        if openfin_response.get('status'):
            openfin_id = open_fin.list_imports(filename=file_name, token=token)
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