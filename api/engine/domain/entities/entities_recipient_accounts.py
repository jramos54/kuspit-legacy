"""data class for recipient information"""
# Librerias Estandar
from dataclasses import dataclass


@dataclass
class RecipientAccount:
    """entity class for recipient Account"""

    idcuenta: int
    cuenta: int
    institucion_bancaria: str
    catalogo_cuenta: str
    is_active: bool
    limite_operaciones: int
    limite: float
    alias: str
