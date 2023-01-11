"""data class for recipient information"""
# Librerias Estandar
from dataclasses import dataclass


@dataclass
class Recipient:
    """entity class for recipient"""

    iddestinatario: int
    nombre: str
    paterno: str
    materno: str
    rfc: str
    curp: str
    is_active: bool
    correo: str
    pfisica: bool
    cuentas: list
