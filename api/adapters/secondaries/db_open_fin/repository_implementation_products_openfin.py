"""Repository implementation for product engine"""
# Librerias Estandar
import typing

# Variables de Configuración
from configuracion.settings import URL_BASE_OPENFIN as OPENFIN_URL

# Librerías de Terceros
import requests

# Proyecto
# Engine
from ....engine.domain.entities.entities_products import Products
from ....engine.use_cases.ports.secondaries import repository_products as repository


class ProductImpl(repository.Product):
    def __init__(self):
        self.url_consulta = "http://" + OPENFIN_URL + "/rpc/productos"

    def get_product(self, id_product: int, token: str) -> [Products, dict]:
        """Obtiene el producto con el id_product"""
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}
        try:
            data = {"datos": {}}
            authorization = {"Authorization": f"Bearer {token}"}
            openfin_response = requests.post(
                self.url_consulta, json=data, headers=authorization
            )

            if openfin_response.status_code == 200:
                products_data = openfin_response.json()

                products_list = products_data["data"]
                product_data = next(
                    (
                        product
                        for product in products_list
                        if product["idproducto"] == id_product
                    ),
                    None,
                )
                product = Products(
                    idproducto=product_data["idproducto"],
                    nombre=product_data["nombre"],
                )
                return product
            else:
                print(openfin_response.json())
                openfin_data = openfin_response.json()
                return openfin_data

        except Exception as e:
            print(f"Error en la respuesta de openfin: \n{e}")
            return openfin_data

    def list_products(self, token: str) -> typing.Union[list, dict]:
        """
        Lista de los productos de una wallet
        """
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}
        try:
            data = {"datos": {}}
            authorization = {"Authorization": f"Bearer {token}"}
            openfin_response = requests.post(
                self.url_consulta, json=data, headers=authorization
            )
            if openfin_response.status_code == 200:
                products_data = openfin_response.json()

                products_list = products_data["data"]

                return products_list
            else:
                print(openfin_response.json())
                openfin_data = openfin_response.json()
                return openfin_data
        except Exception as e:
            print(f"Error en la respuesta de openfin: \n{e}")
            return openfin_data
