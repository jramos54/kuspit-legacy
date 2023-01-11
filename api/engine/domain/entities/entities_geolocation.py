from dataclasses import dataclass
from django.contrib.gis.geos import Point
from datetime import datetime

@dataclass
class GeolocationData:
    """Class for Geolocation Data"""
    user: int
    location: Point  # Usando la clase Point de GeoDjango
    service: str
    timestamp: datetime

