# Librerias Estandar
import typing
from dataclasses import dataclass

from api.engine.use_cases.ports.secondaries import repository_users as repository
from api.engine.use_cases.ports.primaries import manager_users as manager
from api.engine.domain.entities import entities_users as entity


@dataclass
class UserDyPService(manager.UserDyPManager):
    def __init__(self, user_repository: repository.UserDyPRepository):
        self.user_repository = user_repository

    def list_users(self) -> typing.List[entity.UserDyP]:
        return self.user_repository.list_users()

    def get_user(self, id: int) -> entity.UserDyP:
        return self.user_repository.get_user(id=id)

    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        is_persona_fisica: bool,
        is_persona_moral: bool,
    ) -> entity.UserDyP:
        user = self.user_repository.create_user(
            username=username,
            email=email,
            password=password,
            is_persona_fisica=is_persona_fisica,
            is_persona_moral=is_persona_moral,
        )
        return user

    def update_user(
        self,
        id: typing.Optional[int],
        is_active: typing.Optional[bool],
        is_staff: typing.Optional[bool],
        is_superuser: typing.Optional[bool],
        is_customer: typing.Optional[bool],
        is_persona_fisica: typing.Optional[bool],
        is_persona_moral: typing.Optional[bool],
    ) -> entity.UserDyP:
        user = self.user_repository.update_user(
            id=id,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_customer=is_customer,
            is_persona_fisica=is_persona_fisica,
            is_persona_moral=is_persona_moral,
        )
        return user

    def delete_user(
        self,
        id: int,
    ) -> None:
        self.user_repository.delete_user(
            id=id,
        )
        return None
