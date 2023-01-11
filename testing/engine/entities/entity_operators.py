from pydantic import BaseModel, EmailStr
from typing import List

class Permisos(BaseModel):
    perfil: str
    descripcion: str


class Operator(BaseModel):
    idoperador: int
    kasociado: int
    email: str
    ingreso: str
    acceso: bool
    permisos: Permisos
    
class Operators(BaseModel):
    operadores: List[Operator]