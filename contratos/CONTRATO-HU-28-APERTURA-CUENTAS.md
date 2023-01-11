## 1. Apertura de cuenta 

### URL:
```
api/opening_acount/
```

### METHOD:
#### POST

### PARAMS:
```

```

### BODY:
```
CHOICES_CUENTA = [
        ('value1', "AHO"), ahorro
        ('value2', "PRE"), credito
    ]

{
    "count": integer,
    "next": string,
    "previous": string,
    "results": [
            {
                "id":         integer,
                "tipo":       choosefield,
                "idproducto": integer,
            },
        ...
    ]
}

```

### RESPONSE 201:
```
{
    "code": "0",
    "message": "",
    "uuid_control": "097e7d93-4136-44af-8d32-3810c98cb7c1",
    "data": {
        "id":        10002,
        "idcuenta":  296210,
        "fecha": "23/03/2020 15:30:07"
    }
}
```


### RESPONSE 40X:
```
{
    "detail": string
}
```

