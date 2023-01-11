# Contratos Back-Front HU-4-KUSPIT
 
"Yo como usuario de la plataforma de kuspit necesito poder cerrar operaciones"
## => Servicio de cierre de operaciones

## 1. Logout
### URL:
```
api/logout/
```
### METHOD:
#### POST

### PARAMS:
```
{
    username: string,
    access: string
}
````

### BODY:
```
None
````

### RESPONSE 200:
```
{
    message: string
}
```

### RESPONSE 40X:
```
{
    detail: string
}
```

