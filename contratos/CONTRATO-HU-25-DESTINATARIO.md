## 1. Crear detalle de destinatario

### URL:
```
api/destinatario/
```

### METHOD:
#### POST

### PARAMS:
```

```

### BODY:
```
CHOICES_CUENTA = [
        ('value1', "Cuenta Clabe"), #len 18
        ('value2', "Numero de Telefono"), #len 10 
        ('value3', "Numero de Tarjeta"), #len 16
        ('value4', "Numero de Cuenta"), #len 10
    ]

{
    "count": integer,
    "next": string,
    "previous": string,
    "results": [
        {
            "nombre_completo": chardfiel,
            "alias": chardfiel,
            "institucion_bancaria": chardfiel,
            "cuenta": choosefield,
            "limite_de_operaciones": integer,
            "RFC": chardfield,
            "CURP": chardfield,
            "is_active": booleanfild,
            
        },
        ...
    ]
}

```

### RESPONSE 201:
```
{
    "detail": string
}
```


### RESPONSE 40X:
```
{
    "detail": string
}
```

## 2. Obtener detalle de destinatario

### URL:
```
api/destinatario/
```

### METHOD:
#### GET

### PARAMS:
```
?limit=10&offset=0
?openfin_id=1 **administrator**
?idasociado=1-10-4626 **administrator**
"is_active": True,
```

### BODY:
```
None

```

### RESPONSE 200:
```

{
    "count": integer,
    "next": string,
    "previous": string,
    "results": [
        {
           "nombre_completo": chardfiel,
            "alias": chardfiel,
            "institucion_bancaria": chardfiel,
            "cuenta": choosefield,
            "limite_de_operaciones": integer,
            "RFC": chardfield,
            "CURP": chardfield,
            "is_active": booleanfild,
            
        },
        ...
    ]
}
```


### RESPONSE 40X:
```
{
    "detail": string
}
```

## 3. Update/Delete Destinatario

### URL:
```
api/destinatario
```

### METHOD:
#### PUT

### PARAMS:
```
?openfin_id=1 **administrator**
?idasociado=1-10-4626 **administrator**
"is_active": True,
```

### BODY:
```
{
            "nombre_completo": chardfiel,
            "alias": chardfiel,
            "institucion_bancaria": chardfiel,
            "cuenta": choosefield,
            "limite_de_operaciones": integer,
            "RFC": chardfield,
            "CURP": chardfield,
            "is_active": booleanfild,
}
```

### RESPONSE DELETE 204:
```
```

### RESPONSE 202:
```
{
            "nombre_completo": chardfiel,
            "alias": chardfiel,
            "institucion_bancaria": chardfiel,
            "cuenta": choosefield,
            "limite_de_operaciones": integer,
            "RFC": chardfield,
            "CURP": chardfield,
            "is_active": booleanfild,
}
```

### RESPONSE 40X:
```
{
    "detail": string
}
```