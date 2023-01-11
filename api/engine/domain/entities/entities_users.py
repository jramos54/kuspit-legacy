# Librerias Estandar
import typing
from dataclasses import dataclass


@dataclass
class UserDyP:
    id: int
    username: str
    email: str
    is_active: bool
    is_staff: bool
    is_superuser: bool

    is_customer: bool
    is_persona_fisica: bool
    is_persona_moral: bool
    #
    # open_fin_id: typing.Optional[int]
    # payments_user_id: typing.Optional[int]
    #
    # login_attempts: int
    # last_attempt: str | None = None
    #
    # location: str | None = None
    # location_date: str | None = None
    #
    # open_fin_token: str | None = None
