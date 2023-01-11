# Librerías de Terceros
import requests
from django.urls import reverse

# Proyecto
# engine
from ....engine.use_cases.ports.secondaries import repository_beneficiary as repository

OPENFIN_URL = "http://127.0.0.1:8000/"


class BeneficiaryImpl(repository.Beneficiary):
    def create_beneficiary(self, info: dict) -> dict:
        """
        Crea un beneficiario con la info dada
        """
        openfin_data = {"detail": "el proveedor de openfin no respondió exitosamente"}
        try:
            open_fin_url = OPENFIN_URL + reverse("open-fin-mockapi-beneficiary")
            response_openfin = requests.post(open_fin_url, json=info)
            if response_openfin.status_code == 201:
                openfin_data = response_openfin.json()

                # Guardar ID de openfin en la base de datos

                return openfin_data
        except Exception as e:
            print(f"Error {e} en la respuesta de openfin al crear beneficiario")
            return openfin_data

        return openfin_data
