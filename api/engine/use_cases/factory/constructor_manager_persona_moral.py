from api.engine.use_cases.ports.secondaries import (
    repository_persona_moral as repository,
)
from api.engine.use_cases.ports.primaries import manager_persona_moral as manager
from api.engine.use_cases.services import service_persona_moral as service


def constructor_manager_persona_moral(
    persona_moral_repository: repository.PersonaMoral,
) -> manager.PersonaMoral:
    return service.PersonaMoral(persona_moral_repository=persona_moral_repository)
