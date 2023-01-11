# Contratos Back-Front HU-1-DYP
 
"Yo como usuario de la plataforma de PYD necesito obtener la información de mi perfil para poder identificar mis permisos y roles"
## => Servicio de Permisos y Roles
## 1. ListarPermisosyRoles
### URL:
```
api/user/profile
```
### METHOD:
#### GET
### PARAMS:[CONTRATO-HU-1-PYD.md](CONTRATO-HU-1-PYD.md)
```
None
````

### BODY:
```
null
````
 
### RESPONSE 200:
```
{
    profile_info: {
                    name: string,
                    paternal_surname: string,
                    email: string
                   },
    roles: [
            {
                id: integer,
                name: string,
                permissions: [
                                {
                                        id: integer,
                                        name: string
                                },
                                {
                                        id: integer,
                                        name: string
                                },
                                ...
                              ]
            },
            {
                id: integer,
                name: string,
                permissions: [
                                {
                                        id: integer,
                                        name: string
                                },
                                {
                                        id: integer,
                                        name: string
                                },
                                ...
                              ]
            },
            ...
            ...
            ]
}
```

### RESPONSE 40X:
```
{
    detail: string
}
```
