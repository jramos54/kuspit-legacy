# Contratos Back-Front HU-12-CARGA-DE-DOCUMENTOS

## 1. Cargar Documentos
### URL:
```
api/documents/<id:int>
```
El id corresponde al id del tipo de documento que se quiere cargar

### METHOD:
#### POST
### PARAMS:
```
None
```

### BODY:
```
{
    "file_1": document.pdf,
    "file_2": image.jpg,
    "file_3": image.png,
}
```
### RESPONSE 201:
```
{
    [
        {
            "uuid": "f3388804-8a7e-4562-a672-c0bd5aae3794",                         # uuid del documento
            "b64": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAMDAwMDAwQEBAQFBQUFB..."        # base64 del documento
        },
        {
            "uuid": "f3388804-8a7e-4562-a672-c0bd5aae3794",                         # uuid del documento
            "b64": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAMDAwMDAwQEBAQFBQUFB..."        # base64 del documento
        },
        {
            "uuid": "f3388804-8a7e-4562-a672-c0bd5aae3794",                         # uuid del documento
            "b64": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAMDAwMDAwQEBAQFBQUFB..."        # base64 del documento
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

## 2. Listar Documentos

### URL:
```
api/documents
```

### METHOD:
#### GET
### PARAMS:
```
?openfin_id=1 **administrator**
?type_id=1 **administrator**
```

### BODY:
```
None
```

### RESPONSE 200:
```
[
    {
        "uuid": "f3388804-8a7e-4562-a672-c0bd5aae3794",
        "type_id": int,
        "openfin_id": int,
        "b64": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAMDAwMDAwQE..."
    },
    {
        "uuid": "f3388804-8a7e-4562-a672-c0bd5aae3794",
        "type_id": int,
        "openfin_id": int,
        "b64": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAMDAwMDAwQE..."
    },
    {
        "uuid": "f3388804-8a7e-4562-a672-c0bd5aae3794",
        "type_id": int,
        "openfin_id": int,
        "b64": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAMDAwMDAwQE..."
    },
]
```

### RESPONSE 40X:
```
{
    "detail": string
}
```

