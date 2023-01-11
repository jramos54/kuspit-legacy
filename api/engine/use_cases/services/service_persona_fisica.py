from api.engine.use_cases.ports.secondaries import (
    repository_persona_fisica as repository,
)
from api.engine.use_cases.ports.primaries import manager_persona_fisica as manager


class PersonaFisica(manager.PersonaFisica):
    def __init__(self, persona_fisica_repository: repository.PersonaFisica):
        self.persona_fisica_repository = persona_fisica_repository

    def create_persona_fisica(
        self,
        info: dict,
    ) -> dict:
        persona_fisica = self.persona_fisica_repository.create_persona_fisica(
            info=info,
        )
        return persona_fisica

    # def update_persona_fisica(
    #         self,
    #         info: dict,
    #         id: int
    # ) -> dict:
    #     persona_fisica = self.persona_fisica_repository.update_persona_fisica(
    #         info=info,
    #         id=id
    #     )
    #
    #     return persona_fisica
    #
    # def get_persona_fisica(
    #         self,
    #         id: int
    # ) -> dict:
    #     persona_fisica = self.persona_fisica_repository.get_persona_fisica(
    #         id=id
    #     )
    #     return persona_fisica
