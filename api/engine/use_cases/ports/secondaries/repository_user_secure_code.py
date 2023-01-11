# Librerias Estandar
import abc

from api.engine.domain.entities import entities_user_secure_code as entity


class UserSecureCodeRepository(abc.ABC):
    @abc.abstractmethod
    def create_code(
        self,
        user_id: int,
        code: int,
        expedition_datetime: str,
        tries: int,
        is_active: bool,
    ) -> entity.UserSecureCode:
        ...

    @abc.abstractmethod
    def get_code(
        self,
        code: int,
    ) -> entity.UserSecureCode:
        ...

    @abc.abstractmethod
    def update_code(
        self, id: int, code: int, expedition_datetime: str, tries: int
    ) -> entity.UserSecureCode:
        ...
