
## 1. Listar Customers y detalle por queryparams

### URL:
```
api/customers/
```

### METHOD:
#### GET

### PARAMS:
```
?limit=10&offset=0
?persona_fisica=true **administrator**
?persona_moral=true **administrator**
# TODO: revisar si esto es necesario
?openfin_id=1 **administrator**
?payments_id=1 **administrator**
?customer_id=1 **administrator**
```

### BODY:
```
IGNORAR!
{
    "openfin_id": integer,
    "payments_id": integer,
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
            "customer_id": integer,
            "persona_fisica": boolean,
            "persona_moral": boolean,
            "openfin_id": integer,
            "payments_id": integer,
            "openfin_info": dict[openfinserializer],
            "payments_info": dict[paymentserializer],
            
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

## 2. Update/Delete Customer

### URL:
```
api/customers
```

### METHOD:
#### PUT/DELETE

### PARAMS:
```
# TODO: revisar si esto es necesario
?openfin_id=1 **administrator** 
?payments_id=1 **administrator**
?customer_id=1 **administrator**
```

### BODY:
```
{
            "persona_fisica": boolean,
            "persona_moral": boolean,ger,
            "openfin_info": dict[openfinserializer],
            "payments_info": dict[paymentserializer],
}
```

### RESPONSE DELETE 204:
```
```

### RESPONSE 202:
```
{
            "customer_id": integer,
            "persona_fisica": boolean,
            "persona_moral": boolean,
            "openfin_id": integer,
            "payments_id": integer,
            "openfin_info": dict[openfinserializer],
            "payments_info": dict[paymentserializer],
}
```

### RESPONSE 40X:
```
{
    "detail": string
}
```