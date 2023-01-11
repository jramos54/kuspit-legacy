# Librerias Estandar
from dataclasses import dataclass


@dataclass
class Payments:
    kauxiliar: int
    id_recipient: int
    id_account: int
    amount: float
    description: str
    payment_date: str
    reference: str
    payment_hour: str | None = None


@dataclass
class PaymentsOpenFin:
    amount: float
    status: str
    row_id: int
    row_info: str
    payment_date: str
    pactivo: bool
    wactiva: bool
    scheduled_time: str
    alias: str
    programed: bool
    creation_date: str
    intension_date: str
    reference: str
    description: str
    bank_institution: str
    num_account: int
    comision: float
    IVA: float
    total: float
    RFC: str
    CURP: str

    # TODO: solicitar agregar campos,"insitucion bancaria del destinataria","cuenta del destinatario", "numero de cuenta", "comision", "iva", "total".
