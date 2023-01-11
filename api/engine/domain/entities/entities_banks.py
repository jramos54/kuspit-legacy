"""data class for bank information"""
# librerias estandar
# Librerias Estandar
from dataclasses import dataclass


@dataclass
class Bank:
    """entity class for bank"""

    key: int
    nombre: str
    nombre_completo: str
    rfc: str
