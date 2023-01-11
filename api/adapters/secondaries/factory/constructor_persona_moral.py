# Proyecto
from ..db_open_fin.repository_implementation_moral_openfin import PersonaMoralImpl
from ....engine.use_cases.ports.secondaries import (
    repository_persona_moral as repository,
)


def constructor_persona_moral() -> repository.PersonaMoral:
    return PersonaMoralImpl()
