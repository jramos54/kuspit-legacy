"""primary port for recipient"""
# Librerias Estandar
import typing
import abc

# Proyecto
from ....domain.entities.entities_user_dashboard import UserDashboard


class UserDashboardManager(abc.ABC):
    """
    """

    @abc.abstractmethod
    def get_user_dashboard(self, token: str) -> UserDashboard:
        ...

