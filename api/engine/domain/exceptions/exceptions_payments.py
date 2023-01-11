from compartidos.exceptions import ExceptionBase


class FondosInsuficientes(ExceptionBase):
    """Fondos Insuficientes en cuenta"""

    def __init__(self, id_cuenta: int):
        self.id_cuenta = id_cuenta
        self.message = {
            "detail": f"La cuenta {self.id_cuenta} no tiene fondos suficientes para realizar la operacion"
        }
        super().__init__()


class LimiteOperacion(ExceptionBase):
    """Se excedio el limite de operacion"""

    def __init__(self, id_pago: int):
        self.id_pago = id_pago
        self.message = {
            "detail": f"La operacion {self.id_cuenta} excede el limite permitido de operacion"
        }
        super().__init__()


class CuentaSuspendida(ExceptionBase):
    """Mensaje de cuenta suspendida"""

    def __init__(self, id_cuenta: int):
        self.message = {"detail": f"La cuenta {self.id_cuenta} se encuentra suspendida"}
        super().__init__()
