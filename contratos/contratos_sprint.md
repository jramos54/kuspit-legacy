# Contratos Back-Front HU S1-01-M
 
## => CRUDs customers, payments_customers, administrators
## 1. ListarCustomers
### URL:
```
/customers
```
### METHOD:
#### GET
### PARAMS:
```
?customer_id=int
````
el param de customer_id no es obligatorio y sirve para devolver el detalle del customer
### BODY:
```
null
````
 
### RESPONSE:
```
{
    count: 1,
    next: http://next.page,
    previous: null,
    results:
        [
            {
                id: 1,
                name: string,
                paternal_surname: string,
                email: string
            },
            {
                id: 2,
                name: string,
                paternal_surname: string,
                email: string
            },
            {
                id: 3,
                name: string,
                paternal_surname: string,
                email: string
            },
            …
        ]
}
```
La respuesta es páginada teniendo como carga útil el array results.


## 2. ListarPaymentsCustomers
### URL:
```
/payments
```
### METHOD:
#### GET
### PARAMS:
```
?customer_id=int
````

el param de customer_id no es obligatorio y sirve para devolver los pagos del customer

### BODY:
```
null
````
 
### RESPONSE:
```
{
    count: 1,
    next: http://next.page,
    previous: null,
    results:
        [
            {
                id: 1,
                amount: float,
                customer_id: int,
                product_name: string,
                quantity: int
                created_at: datetime,
                updated_at: datetime
            },
            {
                id: 2,
                amount: float,
                customer_id: int,
                product_name: string,
                quantity: int
                created_at: datetime,
                updated_at: datetime
            },
            {
                id: 3,
                amount: float,
                customer_id: int,
                product_name: string,
                quantity: int
                created_at: datetime,
                updated_at: datetime
            },
            …
        ]
}
```


## 3. CrearCustomer
### URL:
```
/customers/
```
### METHOD:
#### POST
### PARAMS:
```
null
````
### BODY:
```
{
    name: string,
    paternal_surname: string,
    email: string
}
````

### RESPONSE:
```
{
    id: 1,
    name: string,
    paternal_surname: string,
    email: string
}
```

## 4. EditarCustomer
### URL:
```
/customers/{id}/
```
### METHOD:
#### PUT
### PARAMS:
```
null
````
### BODY:
```
{
    name: string,
    paternal_surname: string,
    email: string
}
````
### RESPONSE:
```
{
    id: 1,
    name: string,
    paternal_surname: string,
    email: string
}
```

## 5. EliminarCustomer
### URL:
```
/customers/{id}/
```
### METHOD:
#### DELETE
### PARAMS:
```
null
````
### BODY:
```
null
````
### RESPONSE:
```
{
    mensaje: el customer ha sido eliminado
}
```
