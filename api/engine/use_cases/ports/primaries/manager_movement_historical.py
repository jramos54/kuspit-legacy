"""Manager for movement"""
# Librerias Estandar
import typing
import abc

# Proyecto
from ....domain.entities.entities_movement_historical import MovementByMonth


class MovementByMonthManager(abc.ABC):
    """Manager movement"""

    @abc.abstractmethod
    def list_movements_by_month(self, *args, **kwargs) -> typing.List[MovementByMonth]:
        ...
