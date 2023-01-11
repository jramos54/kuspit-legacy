from dataclasses import dataclass

@dataclass
class Permissions:
    # activo: bool
    perfil: str
    descripcion:str

@dataclass
class Operator:
    idoperador: int
    kasociado: int
    nombre: str
    email: str
    ingreso: str
    acceso: bool
    permisos: Permissions


