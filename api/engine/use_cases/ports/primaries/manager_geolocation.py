import typing
import abc

# Proyecto
from ....domain.entities.entities_geolocation import GeolocationData


class GeolocationManager(abc.ABC):
    """Manager movement"""

    @abc.abstractmethod
    def save_geolocation(self, *args, **kwargs):
        ...

