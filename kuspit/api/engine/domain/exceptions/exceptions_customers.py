from compartidos.exceptions import ExceptionBase


class CustomerDoesNotExist(ExceptionBase):
    """Customer does not exist"""

    def __init__(self, customer_id: int):
        self.customer_id = customer_id
        self.message = f"Customer {self.customer_id} does not exist"


class CustomerAlreadyExist(ExceptionBase):
    """Customer already exist"""

    def __init__(self, email: str):
        self.email = email
        self.message = f"email: {self.email} is already assigned to another customer"
