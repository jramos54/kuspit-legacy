"""Exceptions for dates validations"""
from compartidos.exceptions import ExceptionBase


class InvalidDate(ExceptionBase):
    """when user insert a date before current"""

    def __init__(self):
        self.message = {"detail": "La fecha es menor a la fecha actual."}
        super().__init__()


class InvalidHour(ExceptionBase):
    """when user insert a date before current"""

    def __init__(self):
        self.message = {"detail": "La hora es menor a la hora actual actual."}
        super().__init__()


class InvalidSearchDate(ExceptionBase):
    """when a user reverses search dates"""

    def __init__(self):
        self.message = {"detail": "Las fechas de busqueda se encuentran invertidas."}
        super().__init__()
