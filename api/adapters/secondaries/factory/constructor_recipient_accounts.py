# Proyecto
from ..db_open_fin.repository_implementation_recipient_accounts_openfin import (
    RecipientAccountImplementation,
)
from ....engine.use_cases.ports.secondaries import (
    repository_recipient_accounts as repository,
)


def constructor_recipient_account() -> repository.RecipientAccountRepository:
    return RecipientAccountImplementation()
