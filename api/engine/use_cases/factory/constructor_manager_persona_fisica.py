from api.engine.use_cases.ports.secondaries import (
    repository_persona_fisica as repository,
)
from api.engine.use_cases.ports.primaries import manager_persona_fisica as manager
from api.engine.use_cases.services import service_persona_fisica as service


def constructor_manager_persona_fisica(
    persona_fisica_repository: repository.PersonaFisica,
) -> manager.PersonaFisica:
    return service.PersonaFisica(persona_fisica_repository=persona_fisica_repository)
