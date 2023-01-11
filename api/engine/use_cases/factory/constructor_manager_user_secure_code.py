from api.engine.use_cases.ports.secondaries import (
    repository_user_secure_code as repository,
)
from api.engine.use_cases.ports.primaries import manager_user_secure_code as manager
from api.engine.use_cases.services import service_user_secure_code as service


def constructor_manager_user_secure_code(
    user_secure_code_repository: repository.UserSecureCodeRepository,
) -> manager.UserSecureCodeManager:
    return service.UserSecureCodeService(
        user_secure_code_repository=user_secure_code_repository
    )
