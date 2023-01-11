# Librerías de Terceros
from rest_framework import serializers

# Proyecto
from ....engine.domain.exceptions import exceptions_recipient_account as exceptions


class RecipientAccountSerializer(serializers.Serializer):
    """Recipient Serializer"""

    ACCOUNT_OPTION = [
        ("CLABE", "CLABE"),  # len 18
        ("CELULAR", "CELULAR"),  # len 10
        ("TARJETA", "TARJETA"),  # len 16
        ("CUENTA", "CUENTA"),  # len 10
    ]
    account_dict = dict(ACCOUNT_OPTION)

    idcuenta = serializers.IntegerField(required=False)
    institucion_bancaria = serializers.CharField(required=False, allow_blank=True)
    cuenta = serializers.CharField(required=False)
    catalogo_cuenta = serializers.ChoiceField(choices=ACCOUNT_OPTION, required=False)
    limite_operaciones = serializers.IntegerField(required=False, allow_null=True)
    is_active = serializers.BooleanField(required=False)
    limite = serializers.FloatField(required=False, allow_null=True)
    alias = serializers.CharField(max_length=20, required=False, allow_blank=True)

    def validate(self, attrs):
        """Validaciones"""
        if self.partial:
            return attrs

        # longitud de digitos de cuenta segun catalogo
        account_option_values = {
            "CLABE": 18,
            "CELULAR": 10,
            "TARJETA": 16,
            "CUENTA": 10,
        }
        # for destinatario in self.initial_data:
        cuenta_num = attrs.get("cuenta")
        print(
            f"cuenta {cuenta_num} type {type(cuenta_num)} -- {str(attrs.get('cuenta'))}"
        )

        if "catalogo_cuenta" in attrs:
            cuenta_tipo = attrs.get("catalogo_cuenta")

            cuenta_text = self.account_dict[cuenta_tipo]

            if (
                cuenta_tipo == "CUENTA"
                and len(str(cuenta_num)) > account_option_values[cuenta_text]
            ):
                print(f"cuenta tipo {cuenta_tipo}")
                print(
                    f"cuenta num { cuenta_num} > {account_option_values[cuenta_text]}"
                )
                raise exceptions.InvalidLenght

            elif (
                cuenta_tipo != "CUENTA"
                and len(str(cuenta_num)) != account_option_values[cuenta_text]
            ):
                print(f"cuenta tipo {cuenta_tipo}")
                print(f"cuenta num {cuenta_num} > {account_option_values[cuenta_text]}")
                raise exceptions.InvalidLenght

        return attrs


class RecipientAccountQueryParamSerializer(serializers.Serializer):
    idcuenta = serializers.IntegerField(required=False)
    iddestinatario = serializers.IntegerField(required=False)
