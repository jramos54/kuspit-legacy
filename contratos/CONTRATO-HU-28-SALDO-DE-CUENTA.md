## => Servicio de saldo de la cuenta
"Dependiendo del tipo de cuenta se enviara información correspondiente."
## 1. Obtener saldo de la cuenta

### URL:
```
api/cuenta
```

### METHOD:
#### GET

### PARAMS:
```
?openfin_id=1 **administrator**
?cuenta_id=1 **administrator**
```

### BODY:
```
None

```

### RESPONSE 200:
```
**Cuenta AHO**
{
    "code": "0",
    "message": "",
    "uuid_control": "57426b0f-2479-42f4-bace-c347ba6678e5",
    "data": {
        "auxiliar": "1-2002-1",
        "saldo": 200.00,
        "tasa": 4.0,
        "fechaapertura": "2020-07-31"
    }
}
---------------------------------------------------------------------------

**Cuenta PRE**
{
    "code": "0",
    "message": "",
    "uuid_control": "28d9861f-0f18-476d-bce4-1b8a088cfaae",
    "data": {
        "auxiliar": "1-3400-70",
        "saldo": 576998.8800,
        "tasaio": 18.000000,
        "tasaim": 0.000000,
        "plazo": 48,
        "diasxplazo": 30,
        "fpa": "2019-11-27",
        "cat": 0.00,
        "pfijos": true,
        "mismodia": false,
        "issi": true,
        "tipoprestamo": "CONSUMO",
        "planpago": [
            {
                "dt": 34,
                "iva": 1904.00,
                "abono": 7982.23,
                "fecha": "2019-12-31",
                "notas": "",
                "saldo": 700000.00,
                "total": 21786.23,
                "interes": 11900.00
            }, // ...
        ]
    }
}
```


### RESPONSE 40X:
```
{
    "detail": string
}
```