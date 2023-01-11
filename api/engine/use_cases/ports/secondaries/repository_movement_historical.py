"""Manager for movement"""
# Librerias Estandar
import typing
import abc

# Proyecto
from ....domain.entities.entities_movement_historical import MovementByMonth


class MovementByMonthRepository(abc.ABC):
    """Repository for  movement"""

    @abc.abstractmethod
    def list_movements_by_month(self, *args, **kwargs) -> typing.List[MovementByMonth]:
        ...
