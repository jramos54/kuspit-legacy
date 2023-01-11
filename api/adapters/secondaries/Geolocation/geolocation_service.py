from ....engine.domain.entities.entities_geolocation import GeolocationData
from ....engine.use_cases.ports.primaries.manager_geolocation import GeolocationManager
from apps.backoffice.models import users as users_models
from apps.backoffice.models.geolocation_model import Geolocation
from datetime import datetime


class GeolocationService:
    def save_geolocation(self, user, location, service):
        """
        Guarda la geolocalización en la base de datos.
        """
        Geolocation.objects.create(
            user=user,
            location=location,
            service=service,
            timestamp=datetime.now()  # Opcional: se generará automáticamente si se usa auto_now_add en el modelo
        )