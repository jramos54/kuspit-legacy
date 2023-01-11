from api.engine.use_cases.ports.secondaries import repository_users as repository
from api.engine.use_cases.ports.primaries import manager_users as manager
from api.engine.use_cases.services import service_users as service


def constructor_manager_users(
    user_repository: repository.UserDyPRepository,
) -> manager.UserDyPManager:
    return service.UserDyPService(user_repository=user_repository)
