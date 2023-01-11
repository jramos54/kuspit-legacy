# Proyecto
from ..db_open_fin.repository_implementation_fisica_openfin import PersonaFisicaImpl
from ....engine.use_cases.ports.secondaries import (
    repository_persona_fisica as repository,
)


def constructor_persona_fisica() -> repository.PersonaFisica:
    return PersonaFisicaImpl()
