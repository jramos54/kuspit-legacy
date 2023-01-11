# Librerias Estandar
from dataclasses import dataclass


@dataclass
class Accounts:
    alias: str
    type_account: int


@dataclass
class AccountsOpenFin:
    alias: str
    clabe: str
    activo: bool
    saldo: float
    kauxiliar: int
