# Librerias Estandar
from dataclasses import dataclass


@dataclass
class MovementByMonth:
    mes: int
    depositos: float
    retiros: float
    pago_servicios: float
    retiros_programados: float
    current: bool
