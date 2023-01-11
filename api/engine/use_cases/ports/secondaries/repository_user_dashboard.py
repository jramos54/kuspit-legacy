"""secondary port for recipient"""
# Librerias Estandar
import typing
import abc

# Proyecto
from ....domain.entities.entities_user_dashboard import UserDashboard


class UserDashboardRepository(abc.ABC):
    """
    RecipientRepository defines the methods that will use recipent
    """

    @abc.abstractmethod
    def get_user_dashboard(self, token: str) -> UserDashboard:
        ...
