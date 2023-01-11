from pydantic import BaseModel, EmailStr, constr
from typing import List, Optional,Literal

class Product(BaseModel):
    idproducto: int
    nombre: str
    
class Products(BaseModel):
    productos: List[Product]=[]
    
class Wallet(BaseModel):
    alias: str
    clabe: str
    activo: bool
    saldo: float
    kauxiliar: int
    
    
class Wallets(BaseModel):
    wallets: List[Wallet]=[]