# Configurar 2FA

"Yo como usuario de la plataforma DyP necesito configurar el 2FA,  
para poder validar operaciones donde se requiera el 2FA"
## => Servicio para configurar el 2FA
## 1. Generar un OTP
### URL:
```
/api/user/otp/generate
```
### METHOD:
#### POST:
### PARAMS:
```
None
```

### BODY:
```

```

### RESPONSE 200:
```
{
    email: string,
}
```

### RESPONSE 40X:
```
{
    detail: string
}
```

## => Servicio para verificar y habilitar el 2FA
## 2. Verifica un OTP
### URL:
```
/api/user/otp/verify
```
### METHOD:
#### POST:
### PARAMS:
```
None
```

### BODY:
```

```

### RESPONSE 200:
```
{
    email: string,
    token: int,
}
```

### RESPONSE 40X:
```
{
    detail: string
}
```


## => Servicio para validar los tokens TOTP
## 3. valida un OTP
### URL:
```
/api/user/otp/validate
```
### METHOD:
#### POST:
### PARAMS:
```
None
```

### BODY:
```

```

### RESPONSE 200:
```
{
    email: string,
    token: int,
}
```

### RESPONSE 40X:
```
{
    detail: string
}
```

## => Servicio para deshabilitar el 2FA en la cuenta del usuario
## 4. Desahabiliat la funcion 2FA
### URL:
```
/api/user/otp/disable
```
### METHOD:
#### POST:
### PARAMS:
```
None
```

### BODY:
```

```

### RESPONSE 200:
```
{
    email: string,
}
```

### RESPONSE 40X:
```
{
    detail: string
}
```

