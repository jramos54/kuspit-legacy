# Contratos Back-Front HU-23-DYP
 
"Apertura de contrato PF / Pantalla Documentación / Geolocalización"
## => Servicio de gelocalizacion y aceptación de terminos y condiciones
## 1. Reportar Gelocalizacion usuario
### URL:
```
api/users/profile_location
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
    "latitude": float,
    "longitude": float
}
```


 
### RESPONSE 200:
```
{
    "detail": "Tu cuenta se encuentra en proceso de validación.\n Nuestro equipo te informará cuando concluya el proceso y puedas usar tu cuenta.
"
}
```

### RESPONSE 40X:
```
{
    "detail": "Por disposición Oficial requerimos acceder a tu ubicación geográfica. La información que nos proporciones no se utilizará para ningún otro propósito.
¿Cómo compartir tu ubicación geográfica?
Consulta en el menú de tu navegador con la opción Configuración y selecciona Compartir ubicación.
Recuerda autorizar el dispositivo (computadora tablet) que uses para ingresar a DyP para Compartir ubicación.
Te sugerimos volver a cargar la página actual para que se aplique correctamente la autorización de tu ubicación geográfica."
}
```
