# Contratos Back-Front HU-3-KUSPIT
 
"Yo como usuario de la plataforma de DyP necesito poder realizar pagos de servicios"
## => 
## 1. Agregar Solicitudes de pago
### URL:
```
api/payments/add-payment-thirdparty
```
### METHOD:
#### POST
### PARAMS:
```
none
````

### BODY:
```
{
    fecha_pago: datetime,
    numero_cuenta: int,
    destinatario:string,
    importe:float,
    referencia:string,
    concepto:stirng,
    fecha_vencimiento:datetime,
    confirmacion : Bool   
}
````
 
### RESPONSE 201:
```
{
    id_pago: int,
    fecha_pago: datetime,
    numero_cuenta: int,
    destinatario:string,
    importe:float,
    referencia:string,
    concepto:stirng,
    fecha_vencimiento:datetime    
}
```

### RESPONSE 40X:
```
{
    detail: string
}
```

## 2. Confirmacion Pago
### URL:
```
api/payments/confirmation-payment
```
### METHOD:
#### PUT

### PARAMS:
```
{
        id_pago: int,
}
````

### BODY:
```
{
    id_pago: int,
    fecha_pago: datetime,
    numero_cuenta: int,
    destinatario: string,
    importe: float,
    referencia: string,
    concepto: stirng,
    fecha_vencimiento: datetime,  
    confirmacion: boolean  
}
````

### RESPONSE 200:
```
{
    id_pago: int,
    fecha_pago: datetime,
    numero_cuenta: int,
    destinatario: string,
    importe: float,
    referencia: string,
    concepto: stirng,
    fecha_vencimiento: datetime,  
    confirmacion: boolean  
}
```

### RESPONSE 40X:
```
{
    detail: string
}
```


## 5. Consultar movimientos de la cuenta

### URL:
```
api/payments/account-movements
```

### METHOD:
#### GET

### PARAMS:
```
{id_cuenta: int}
````

### BODY:
```
{
  [{id_pago: int,
    fecha_pago: datetime,
    numero_cuenta: int,
    destinatario: string,
    importe: float,
    referencia: string,
    concepto: stirng,
    fecha_vencimiento: datetime,  
    confirmacion: boolean
    }]
}
````

### RESPONSE 201:
```
{
  [{id_pago: int,
    fecha_pago: datetime,
    numero_cuenta: int,
    destinatario: string,
    importe: float,
    referencia: string,
    concepto: stirng,
    fecha_vencimiento: datetime,  
    confirmacion: boolean
    }]
}
```

### RESPONSE 40X:
```
{
    detail: string
}
```
## 4. Crear pago de servicio

### URL:
```
api/payments/payment-service
```

### METHOD:
#### POST

### PARAMS:
```
None
````

### BODY:
```
{
  "biller_id": 96652,
  "account_number": "321654871238120",
  "amount": 12.21,
  "currency": "MXN",
  "external_id": "84bce950-c878-483e-aeca-41217f969301",
  "pos_number": "S12C03"
}
````

### RESPONSE 201:
```
{
  "type": "transaction",
  "id": 2681173116846,
  "amount": 5568,
  "amount_currency": "MXN",
  "fx_rate": 18.2569,
  "amount_usd": 304.98,
  "transaction_fee": 3,
  "total_usd": 307.98,
  "hours_to_fulfill": 48,
  "created_at": "2018-07-15T17:35:31Z",
  "status": "fulfilled",
  "external_id": "d3a884c0-5dc2-4519-b280-1ac0a4592b90",
  "ticket_text": "Authorization 6523d5dfc5b",
  "account_number": "51763518635146"
}
```

### RESPONSE 40X:
```
{
    detail: string
}
```

## 6. Crear Notificaciones de pago

### URL:
```
api/payments/payment-notifications
```

### METHOD:
#### GET

### PARAMS:
```
{
    "biller_id": int
}
````

### BODY:
```
{
  "biller_id": 96652,
  "account_number": "321654871238120",
  "amount": 12.21,
  "currency": "MXN",
  "external_id": "84bce950-c878-483e-aeca-41217f969301",
  "pos_number": "S12C03"
}
````

### RESPONSE 201:
```
{
  "type": "transaction",
  "id": 2681173116846,
  "amount": 5568,
  "amount_currency": "MXN",
  "fx_rate": 18.2569,
  "amount_usd": 304.98,
  "transaction_fee": 3,
  "total_usd": 307.98,
  "hours_to_fulfill": 48,
  "created_at": "2018-07-15T17:35:31Z",
  "status": "fulfilled",
  "external_id": "d3a884c0-5dc2-4519-b280-1ac0a4592b90",
  "ticket_text": "Authorization 6523d5dfc5b",
  "account_number": "51763518635146"
}
```

### RESPONSE 40X:
```
{
    detail: string
}
```