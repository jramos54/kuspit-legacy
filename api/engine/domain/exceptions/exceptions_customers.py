from compartidos.exceptions import ExceptionBase


class CustomerDoesNotExist(ExceptionBase):
    """Customer does not exist"""

    def __init__(self, customer_id: int):
        self.customer_id = customer_id
        self.message = {"detail": f"Customer {self.customer_id} does not exist"}
        super().__init__()


class CustomerAlreadyExist(ExceptionBase):
    """Customer already exist"""

    def __init__(self, email: str):
        self.email = email
        self.message = {
            "detail": f"email: {self.email} is already assigned to another customer"
        }
        super().__init__()


class InvalidRFC(ExceptionBase):
    """Invalid RFC"""

    def __init__(self):
        self.message = {
            "detail": "El RFC no cumple con los requerimientos oficiales para ser aceptada"
        }
        super().__init__()


class InvalidPhoneNumber(ExceptionBase):
    """Invalid phone number lenght"""

    def __init__(self):
        self.message = {
            "detail": "El numero de telefono no cumple con los requerimientos para ser aceptado"
        }
        super().__init__()


class NotBank(ExceptionBase):
    """No bank declared for bank account"""

    def __init__(self):
        self.message = {"detail": "Debe especificarse el banco para la cuenta CLABE"}
        super().__init__()


class InvalidClabeAccount(ExceptionBase):
    """Invalid CLABE account"""

    def __init__(self):
        self.message = {"detail": "La cuenta CLABE no es valida"}
        super().__init__()


class InvalidCurp(ExceptionBase):
    """Invalid RFC"""

    def __init__(self):
        self.message = {
            "detail": "La CURP no cumple con los requerimientos oficiales para ser aceptada"
        }
        super().__init__()


class InvalidYearOfBirth(ExceptionBase):
    """Customer is younger"""

    def __init__(self):
        self.message = {"detail": "Debes ser mayor de edad"}
        super().__init__()
