"""Service for recipient"""
# Librerias Estandar
import typing

# Proyecto
from ...use_cases.ports import secondaries as repository
from ...use_cases.ports import primaries as manager
from ...domain.entities import entities_user_dashboard as entity


class UserDashboardService(manager.UserDashboardManager):
    """RecipientService defines the methods"""

    def __init__(self, user_dashboard_repository: repository.UserDashboardRepository):
        self.user_dashboard_repository = user_dashboard_repository

    def get_user_dashboard(self, token: str) -> entity.UserDashboard:
        """return a recipient by id"""

        recipient = self.user_dashboard_repository.get_user_dashboard(
            token=token
        )
        return recipient
