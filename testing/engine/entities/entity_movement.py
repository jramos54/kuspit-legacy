from pydantic import BaseModel, EmailStr, constr
from typing import List, Optional,Literal

class Movement(BaseModel):
    fecha_elaboracion: str
    fecha_pago: Optional[str] = None
    movimiento: Literal['Depósito', 'Retiro', 'Servicio','Impuesto']
    estatus: Literal['Pendiente', 'Enviada', 'Liquidado','Enviado', 'Liquidada','Cancelada','Cancelado']
    destinatario: str
    cuenta_bancaria: str
    monto: float
    concepto: str
    clave_rastreo: Optional[str] = None
    referencia: Optional[str] = None
    info: Optional[str] = None
    
class Movements(BaseModel):
    movimientos: List[Movement]=[]
    
class HistoricalMovement(BaseModel):
    mes: int
    retiros: float
    depositos: float
    current: bool
    
    
class HistoricalMovements(BaseModel):
    movimientos: List[HistoricalMovement]=[]