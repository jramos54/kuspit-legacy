from api.engine.use_cases.ports.secondaries import (
    repository_persona_moral as repository,
)
from api.engine.use_cases.ports.primaries import manager_persona_moral as manager


class PersonaMoral(manager.PersonaMoral):
    def __init__(self, persona_moral_repository: repository.PersonaMoral):
        self.persona_moral_repository = persona_moral_repository

    def create_persona_moral(
        self,
        info: dict,
    ) -> dict:
        persona_moral = self.persona_moral_repository.create_persona_moral(
            info=info,
        )
        return persona_moral

    # def update_persona_moral(
    #         self,
    #         info: dict,
    #         id: int
    # ) -> dict:
    #     persona_moral = self.persona_moral_repository.update_persona_moral(
    #         info=info,
    #         id=id
    #     )

    #     return persona_moral

    # def get_persona_moral(
    #         self,
    #         id: int
    # ) -> dict:
    #     persona_moral = self.persona_moral_repository.get_persona_moral(
    #         id=id
    #     )
    #     return persona_moral
