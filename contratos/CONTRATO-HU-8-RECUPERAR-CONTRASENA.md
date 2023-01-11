# Contratos Back-Front HU-8-DYP

"Recuperar contraseña / validaciones Mail"
## => Servicio para comprobar que existe un usuario con el correo y enviar codigo de 6 digitos
## 1. Recuperar contrasena
### URL:
```
api/users/reset-password
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
    email: string,
    code: string,
}
````

### RESPONSE 200:
```
{
    detail: string,

}
```

### RESPONSE 40X:
```
{
    detail: string
}
```

## => Servicio validar el codigo de 6 digitos
## 2. Confirmar codigo
### URL:
```
api/users/reset-code-confirm
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
    email: string,
    code: string,
}
````

### RESPONSE 200:
```
{
    detail: string,

}
```

### RESPONSE 40X:
```
{
    detail: string
}
```

"Recuperar contraseña / Confirmación de contraseña"
## => Servicio para confirmar el cambio de contraseña y validar token 2fa
## 3. Confirmar contrasenas
### URL:
```
api/users/reset-password
```
### METHOD:
#### PUT

### PARAMS:
```
None
````

### BODY:
```
{
    password: string,
    confirm_password: string,
    token_2fa: string,
}
````

### RESPONSE 200:
```
{
    detail: string,

}
```

### RESPONSE 40X:
```
{
    detail: string
}
```