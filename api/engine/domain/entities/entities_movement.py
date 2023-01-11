# Librerias Estandar
from dataclasses import dataclass


@dataclass
class Movement:
    """Class for movement"""

    fecha_elaboracion: str
    fecha_pago: str
    movimiento: str
    estatus: str
    destinatario: str
    cuenta_bancaria: int
    monto: float
    concepto: str
    clave_rastreo: str
    referencia: str
    info: str
    pfisica: bool
    institucion_bancaria: str
