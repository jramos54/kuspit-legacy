"""factory of recipient"""
# Proyecto
from ...use_cases.ports import secondaries as repository
from ...use_cases.ports import primaries as manager
from ...use_cases import services as service


def constructor_manager_user_dashboard(
    user_dashboard_repository: repository.UserDashboardRepository,
) -> manager.UserDashboardManager:
    return service.UserDashboardService(user_dashboard_repository)
