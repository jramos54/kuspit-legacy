import os
from celery import Celery

# # Ajusta la configuración para que use el nombre del directorio actual
# current_directory = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
# app = Celery(current_directory)
#
# # Continuar con la configuración de Celery
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuracion.settings')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()

# Configura la variable de entorno para Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuracion.settings')

# Crea la aplicación Celery con un nombre estático
app = Celery('DyP_front_2')

# Cargar la configuración de Celery desde el archivo settings.py usando el prefijo CELERY
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubrir automáticamente las tareas en todas las aplicaciones instaladas de Django
app.autodiscover_tasks(['api.adapters.primaries.recipients_batch',
                        'api.adapters.primaries.payments_batch'])