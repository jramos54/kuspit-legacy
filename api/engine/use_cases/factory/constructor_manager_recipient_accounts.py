"""factory of recipient"""
# Proyecto
from ...use_cases.ports import secondaries as repository
from ...use_cases.ports import primaries as manager
from ...use_cases import services as service


def constructor_manager_recipient_account(
    recipient_account_repository: repository.RecipientAccountRepository,
) -> manager.RecipientAccountManager:
    return service.RecipientAccountService(recipient_account_repository)
