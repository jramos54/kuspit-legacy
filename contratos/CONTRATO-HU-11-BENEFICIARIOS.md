# Contratos Back-Front HU-11-BENEFICIARIOS

"Yo como usuario de la plataforma de kuspit necesito poder crear, actualizar, eliminar uno o varios beneficiarios"

## 1. Crear Beneficiarios
### URL:
```
api/beneficiarios/
```

### METHOD:
#### POST
### PARAMS:
```
None
```

### BODY:
```
{
    "user_id": integer,
    "beneficiarios":[ 
                        {
                        "apellido_paterno":       "Vargas",
                        "apellido_materno":       "Torres",
                        "nombre":                 "Pedro",
                        "fecha_de_nacimiento":    "03/02/1990",
                        "domicilio":  {
                                            "calle":       "unacalle",
                                            "colonia":     "unacolonia",
                                            "numint":      "02",
                                            "numext":      "01",
                                            "municipio":   "unmunicipio pm",
                                            "pais":        "unpais pm"
                                            "cp":          "65900",
                        },
                        "parentesco":             "hermano",
                        "porcentaje":             "100",
                        }
                    ]
}
```
### RESPONSE 201:
```
{
    "user_id": integer,
    "contrato_id": integer,
    "beneficiarios":[ 
                        {
                        "apellido_paterno":       "Vargas",
                        "apellido_materno":       "Torres",
                        "nombre":                 "Pedro",
                        "fecha_de_nacimiento":    "03/02/1990",
                        "domicilio":  {
                                            "calle":       "unacalle",
                                            "colonia":     "unacolonia",
                                            "numint":      "02",
                                            "numext":      "01",
                                            "municipio":   "unmunicipio pm",
                                            "pais":        "unpais pm"
                                            "cp":          "65900",
                        },
                        "parentesco":             "hermano",
                        "porcentaje":             "100",
                        }
                    ]
}
```

### RESPONSE 40X:
```
{
    detail: string
}
```

## 1. Listar Beneficiario

### URL:
```
api/beneficiarios/
```

### METHOD:
#### GET
### PARAMS:
```
?limit=10&offset=0
# TODO: revisar si esto es necesario
?openfin_id=1 **administrator**
?contrato_id=1 **administrator**
?customer_id=1 **administrator**
```

### BODY:
```
IGNORAR!
{
    "openfin_id": integer,
    "contrato_id": integer,
    "customer_id": integer,

}
```

### RESPONSE 200:
```
{
    "count": integer,
    "next": string,
    "previous": string,
    "results": [
        {
            "contrato_id": int,
            "customer_id": int,
            "beneficiarios": dict[beneficiariosserializer],
            
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

## 3. Update/Delete Customer

### URL:
```
api/beneficiarios/
```

### METHOD:
#### PUT/DELETE
### PARAMS:
```
# TODO: revisar si esto es necesario
?contrato_id=1 **administrator** 
?payments_id=1 **administrator**
?customer_id=1 **administrator**
```

### BODY:
```
IGNORAR!
{
            "contrato_id": int,
            "customer_id": int,
            "beneficiarios": dict[beneficiariosserializer],

}
```

### RESPONSE 200:
```
{
    "count": integer,
    "next": string,
    "previous": string,
    "results": [
        {
            "contrato_id": int,
            "customer_id": int,
            "beneficiarios": dict[beneficiariosserializer],
            
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