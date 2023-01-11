from compartidos.exceptions import ExceptionBase


class RecipientDoesNotExist(ExceptionBase):
    """Recipient does not exist"""

    def __init__(self, recipient_id: int):
        self.recipient_id = recipient_id
        self.message = {"detail": f"Recipient {self.recipient_id} does not exist"}
        super().__init__()


class RecipientAlreadyExist(ExceptionBase):
    """Recipient already exist"""

    def __init__(self):
        self.message = {"detail": f"El destinatario ya existe"}
        super().__init__()


class InvalidRFC(ExceptionBase):
    def __init__(self):
        self.message = {"detail": f"El RFC proporcionado esta mal construido"}
        super().__init__()


class InvalidCURP(ExceptionBase):
    def __init__(self):
        self.message = {"detail": f"El CURP proporcionado esta mal construido"}
        super().__init__()
