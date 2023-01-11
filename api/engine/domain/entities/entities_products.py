"""data class for product information"""
# Librerias Estandar
from dataclasses import dataclass


@dataclass
class Products:
    """entity class for product"""

    idproducto: int
    nombre: str
