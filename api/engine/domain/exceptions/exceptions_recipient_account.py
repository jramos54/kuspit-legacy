from compartidos.exceptions import ExceptionBase


class InvalidLenght(ExceptionBase):
    def __init__(self):
        self.message = {
            "detail": f"La cuenta proporcionada no cumple con el formato requerido"
        }
        super().__init__()
