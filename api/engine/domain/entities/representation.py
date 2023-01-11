# Librerias Estandar
import datetime
import uuid
import json
from decimal import Decimal


class RepresentationServerMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self) -> str:
        return self.json_str()

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def to_json(obj):
        representation = None

        if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
            representation = obj.isoformat()

        if representation.endswith("+00:00"):
            representation = representation[:-6] + "Z"

            return representation

        if isinstance(obj, uuid.UUID):
            return obj.hex

        if isinstance(obj, Decimal):
            return str(obj)
        else:
            return obj.__dict__

    def json(self):
        return json.loads(self.json_str())

    def json_str(self):
        return json.dumps(self, default=lambda o: self.to_json(o))
