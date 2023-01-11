# Contratos Back-Front HU-1-KUSPIT
 
"Yo como usuario de la plataforma de kuspit necesito poder crear un usuario ya se administrador o cliente"
## => Servicio de Crear Usuario
## 1. CrearUsuario
### URL:
```
api/users/create
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
    username: string,
    email: string,
    password: string,
    is_staff: boolean,
    is_customer: boolean,
    is_persona_fisica: boolean,
    is_persona_moral: boolean
}
```
 
### RESPONSE 201:
```
{
    id: integer,
    username: string,
    email: string,
    password: string,
    is_staff: boolean,
    is_customer: boolean,
    is_persona_fisica: boolean,
    is_persona_moral: boolean
}
```

### RESPONSE 40X:
```
{
    detail: string
}
```

## 2. Login
### URL:
```
api/token/
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
    username: string,
    password: string
}
```

### RESPONSE 200:
```
{
    refresh: string,
    access: string
}
```

### RESPONSE 40X:
```
{
    detail: string
}
```

## 1. Crear Perfil Persona Moral

### URL:
```
api/users/onboarding/persona_moral/
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
    "openfin_info": {
                        "idsucursal": "1",
                        "idrol":      "10",
                        "empresa":    "Persona Moral",
                        "domicilio":  {
                                            "calle":       "unacalle pm",
                                            "numext":      "01",
                                            "numint":      "02",
                                            "colonia":     "unacolonia pm",
                                            "municipio":   "unmunicipio pm",
                                            "cp":          "65900",
                                            "estado":      "unestado pm",
                                            "entrecalles": "algunasentrecalles",
                                            "pais":        "unpais pm"
                        },
                        "telefono":           "1234567890",
                        "fecha_constitucion": "03/02/2021",
                        "pais_nacionalidad":  "México",
                        "rfc":                "1234567890123",
                        "idgiro":             "1"
    } 

}
```

### RESPONSE 201:
```
{
    "id": integer,
    "user_id": integer,
    "openfin_info": {
                        "idsucursal":   "1",
                        "idrol":        "10",
                        "empresa":      "Persona Moral",
                        "domicilio":    {
                                            "calle":       "unacalle pm",
                                            "numext":      "01",
                                            "numint":      "02",
                                            "colonia":     "unacolonia pm",
                                            "municipio":   "unmunicipio pm",
                                            "cp":          "65900",
                                            "estado":      "unestado pm",
                                            "entrecalles": "algunasentrecalles",
                                            "pais":        "unpais pm"
                        },
                        "telefono":           "1234567890",
                        "fecha_constitucion": "03/02/2021",
                        "pais_nacionalidad":  "México",
                        "rfc":                "1234567890123",
                        "idgiro":             "1"
    }
}
```

### RESPONSE 40X:
```
{
    detail: string
}
```

## 2. Crear perfil de cliente persona fisica
### URL:
```
api/users/onboarding/persona_fisica
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
    "openfin_info": {"nombre":             "Fulano",
                        "paterno":            "Rivera",
                        "materno":            "Rios",
                        "sexo":               "0",
                        "fechanacimiento":    "30/09/1992",
                        "lugarnacimiento":    {
                                                  "municipio": "Monterrey",
                                                  "estado": "Nuevo León",
                                                  "pais": "México"
                                                },
                        "pais_nacionalidad":  "1", 
                        "claveelector":       "123123123ssa2233", 
                        "domicilio": {
                                      "calle":            "unacalle",
                                      "numext":           "unnumext",
                                      "numint":           "unnumint",
                                      "colonia":          "unacolonia",
                                      "cp":               "uncp",
                                      "municipio":        "unmunicipio",
                                      "estado":           "unestado",
                                      "entrecalles":      "algunasentrecalles",
                                      "pais":             "nombredelpais"
                                    },
                        "profesion":          "0",
                        "ocupacion":          "0",
                        "rfc":                "1234567890123",
                        "curp":               "123456789012345678",
                        "email":              "unemail",
                        "telefono":           "8117480407",
                        "idsucursal":         "1",
                        "idrol":              "10",
                        "estadocivil":        "0"
                        }
}
```

### RESPONSE 201:
```
{
    "id": integer,
    "user_id": integer,
    "openfin_info": {
                        "nombre":             "Fulano",
                        "paterno":            "Rivera",
                        "materno":            "Rios",
                        "sexo":               "0",
                        "fechanacimiento":    "30/09/1992",
                        "lugarnacimiento":    {
                                                    "municipio": "Monterrey",
                                                    "estado": "Nuevo León",
                                                    "pais": "México"
                                            },
                        "pais_nacionalidad":  "1", 
                        "claveelector":   "123123123ssa2233", 
                        "domicilio": {
                                          "calle":            "unacalle",
                                          "numext":           "unnumext",
                                          "numint":           "unnumint",
                                          "colonia":          "unacolonia",
                                          "cp":               "uncp",
                                          "municipio":        "unmunicipio",
                                          "estado":           "unestado",
                                          "entrecalles":      "algunasentrecalles",
                                          "pais":             "nombredelpais"
                        },
                        "profesion":          "0",
                        "ocupacion":          "0",
                        "rfc":                "1234567890123",
                        "curp":               "123456789012345678",
                        "email":              "unemail",
                        "telefono":           "8117480407",
                        "idsucursal":         "1",
                        "idrol":              "10",
                        "estadocivil":        "0"
                        }

}
```

### RESPONSE 40X:
```
{
    "detail": string
}
```
