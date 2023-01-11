# Proyecto
from ..db_open_fin.repository_implementation_recipient_openfin import (
    RecipientImplementation,
)
from ....engine.use_cases.ports.secondaries import repository_recipient as repository


def constructor_recipient() -> repository.RecipientRepository:
    return RecipientImplementation()
