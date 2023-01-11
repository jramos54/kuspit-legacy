# Librerias Estandar
from dataclasses import dataclass

# Librerías de Terceros
from django.utils import timezone


@dataclass
class UserSecureCode:
    id: int
    user_id: int
    code: int
    expedition_datetime: str
    tries: int
    is_active: bool

    @property
    def expired_code(self):
        return ((timezone.now() - self.expedition_datetime).total_seconds() / 60) >= 10
