"""data class for recipient information"""
# Librerias Estandar
from dataclasses import dataclass


@dataclass
class UserDashboard:
    """entity class for recipient"""
    nombre: str
    correo: str
    kasociado: int


