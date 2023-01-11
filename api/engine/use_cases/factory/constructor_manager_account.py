from api.engine.use_cases.ports.secondaries import repository_account as repository
from api.engine.use_cases.ports.primaries import manager_account as manager
from api.engine.use_cases.services import service_account as service


def constructor_manager_account(
    account_repository: repository.Account,
) -> manager.Account:
    return service.Account(account_repository=account_repository)
