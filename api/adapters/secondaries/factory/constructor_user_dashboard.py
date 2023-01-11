# Proyecto
from ..db_open_fin.repository_implementation_user_dashboard_openfin import (
    UserDashboardImplementation,
)
from ....engine.use_cases.ports.secondaries import repository_user_dashboard as repository


def constructor_user_dashboard() -> repository.UserDashboardRepository:
    return UserDashboardImplementation()
