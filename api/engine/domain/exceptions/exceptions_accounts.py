"""Exceptions for opening account service"""
from compartidos.exceptions import ExceptionBase


class AccountAlreadyExist(ExceptionBase):
    """Account already exist"""

    def __init__(self, alias: str):
        self.alias = alias
        self.message = {
            "detail": f"The account with the alias: {self.alias} already exist."
        }
        super().__init__()


class AccountDoesnotExist(ExceptionBase):
    """Account already exist"""

    def __init__(self, alias: str):
        self.alias = alias
        self.message = {
            "detail": f"The account with the alias: {self.alias} does not exist."
        }
        super().__init__()
