from pydantic import BaseModel, EmailStr
from typing import List, Optional

class Bank(BaseModel):
    key: int
    nombre: str
    nombre_completo: Optional[str] = None
    rfc: Optional[str] = None
    
class Banks(BaseModel):
    bancos: List[Bank]