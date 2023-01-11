"""Exceptions for products service"""
from compartidos.exceptions import ExceptionBase


class ProductDoesNotExist(ExceptionBase):
    """Product does not exist"""

    def __init__(self, id_producto: str):
        self.id_producto = id_producto
        self.message = {
            "detail": f"The product with the idproduct: {self.id_producto} does not exist."
        }
        super().__init__()
