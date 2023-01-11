""" repository to conect to openfin"""
# Librerias Estandar
import collections
import json
import typing
from datetime import datetime

# Variables de Configuración
from configuracion.settings import URL_BASE_OPENFIN as OPENFIN_URL

# Librerías de Terceros
import requests
from dateutil.relativedelta import relativedelta

# Proyecto
from ....engine.domain.entities.entities_movement_historical import MovementByMonth
from ....engine.use_cases.ports.secondaries import (
    repository_movement_historical as repository,
)

import requests
import json
import collections
from datetime import datetime
from dateutil.relativedelta import relativedelta
from rest_framework.exceptions import ValidationError


class MovementsByMonthImplementation(repository.MovementByMonthRepository):
    def __init__(self):
        self.url_consulta = "http://" + OPENFIN_URL + "/rpc/cuenta_movimientos"

    def list_movements_by_month(self, *args, **kwargs) -> typing.List[MovementByMonth]:
        token = args[0] if args else None
        kauxiliar = kwargs.get("kauxiliar", None)
        authorization = {"Authorization": token}

        today = datetime.now()
        last_date = today - relativedelta(months=11)
        initial_date = last_date.replace(day=1)

        defecha = initial_date.strftime("%d/%m/%Y")
        afecha = today.strftime("%d/%m/%Y")

        data = {
            "datos": {
                "kauxiliar": kauxiliar,
                "defecha": defecha,
                "afecha": afecha,
                "limite": 0,
            }
        }

        try:
            openfin_response = requests.post(self.url_consulta, json=data, headers=authorization)
            openfin_response.raise_for_status()  # Esto lanzará un error si el status_code no es 200
            openfin_content = openfin_response.json()

            if openfin_content.get("data") is None:
                return []
            else:
                list_movements = openfin_content["data"].get("movimientos", [])
                historical_data = self.historical_totals(*list_movements)
                return historical_data

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return {"error": f"HTTP error: {http_err}"}
        except requests.exceptions.RequestException as req_err:
            print(f"Request exception: {req_err}")
            return {"error": f"Request exception: {req_err}"}
        except Exception as error_exception:
            print(f"Unexpected error: {error_exception}")
            return {"error": f"Unexpected error: {error_exception}"}

    def historical_totals(self, *movements):
        # Mapeo para el renombre de claves
        mapping = {
            "Depósito": "depositos",
            "Retiro": "retiros",
            "Retiros Programados": "retiros_programados",
            "Pago de Servicios": "pago_servicios",
        }
        print(f"{type(movements)} - {len(movements)}")

        monthly_totals = collections.defaultdict(lambda: collections.defaultdict(float))
        today = datetime.today()
        current_month = today.month

        try:
            for movement in movements:
                movement_type = movement.get("movimiento")
                amount = movement.get("monto")
                status = movement.get("estatus")
                fecha_pago = movement.get("fecha_pago")

                if fecha_pago is None:
                    # print(f"Fecha de pago es None en el movimiento: {movement}")
                    continue  # Saltar movimientos con fecha None

                date_payment = datetime.strptime(fecha_pago, "%Y-%m-%d")

                if (
                        status in ["Enviada", "Liquidado"]
                        and movement_type in ["Depósito", "Retiro", "Pago de Servicios"]
                ) or (status == "Pendiente" and movement_type == "Retiros Programados"):
                    renamed_movement_type = mapping.get(movement_type, movement_type)
                    monthly_totals[date_payment.month][renamed_movement_type] += amount

            print(f"roll out movements OK")
            # Redondear los valores y preparar la lista de resultados, ordenando por mes
            result = []
            for month, totals in sorted(monthly_totals.items()):
                rounded_totals = {k: round(v, 2) for k, v in totals.items()}
                result.append(
                    {"mes": month, **rounded_totals, "current": month == current_month}
                )

            return result

        except Exception as error_exception:
            print(f"Error processing movements: {error_exception}")
            raise ValidationError(f"Error processing movements: {error_exception}")
