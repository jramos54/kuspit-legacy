# Librerias Estandar
from dataclasses import dataclass


@dataclass
class Beneficiary:
    nombre: str
    paterno: str
    materno: str
    fecha_nacimiento: str
    calle: str
    numext: str
    numint: str
    pais: str
    estado: str
    ciudad: str
    alcaldia: str
    cp: str
    parentesco: str
    porcentaje: str
