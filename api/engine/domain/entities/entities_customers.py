# import typing
# Librerias Estandar
from dataclasses import dataclass


@dataclass
class Customer:
    id: int
    name: str
    paternal_surname: str
    email: str
