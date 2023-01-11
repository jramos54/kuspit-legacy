# Librerias Estandar
import typing
import abc

from api.engine.domain.entities import entities_users as entity


class UserDyPManager(abc.ABC):
    @abc.abstractmethod
    def list_users(self) -> typing.List[entity.UserDyP]:
        ...

    @abc.abstractmethod
    def get_user(self,id:str) -> entity.UserDyP:
        ...

    @abc.abstractmethod
    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        is_persona_fisica: bool,
        is_persona_moral: bool,
    ) -> entity.UserDyP:
        ...

    @abc.abstractmethod
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
        ...

    @abc.abstractmethod
    def delete_user(
        self,
        id: int,
    ) -> None:
        ...
