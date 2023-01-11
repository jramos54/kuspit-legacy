from pydantic import BaseModel, EmailStr
from typing import List

class Recipient(BaseModel):
    iddestinatario: int
    nombre: str
    paterno: str
    materno: str
    rfc: str
    curp: str
    is_active: bool
    correo: EmailStr
    pfisica: bool
    cuentas: List[str]
    
class Recipients(BaseModel):
    destinatarios: List[Recipient]