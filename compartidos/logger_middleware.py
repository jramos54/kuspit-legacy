import time
from django.conf import settings
import logging

class ApiLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        if settings.ENABLE_API_LOGGING:
            start_time = time.time()
            response = self.get_response(request)
            end_time = time.time()
            duration = round(end_time - start_time, 2)  # Redondeo a 2 decimales
            self.logger.info(f"=> Solicitud al servicio {request.path} tomo {duration} Segundos")
            return response
        else:
            return self.get_response(request)