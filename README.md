# API django_assesment
En este proyecto se implementa una API REST con arquitectura hexagonal y desarrollo basado en unittest de compoortamieto.

## Clonar repositorio

```
git clone https://github.com/nxiodev/django_arq_hex_example
```

## Bases de datos:
- **PostgreSQL** : Se utiliza para almacenar la información interna de la aplicación

`NOTA: De acuerdo a lo propuesto en la HU_SPRINT.md se genera un diagrama de entidad relación en un png`

## Desplegar proyecto

1. Crea tu ambiente virtual ejecuta el siguiente comando

   ```ssh
   py -m venv venv;
   venv\Scripts\activate
   ```

2. Instala las dependencias del proyecto

   ```ssh
    pip install -r requirements.txt
    ```

3. Crear una base de datos paycode-db en postgres y situate en la carpeta django_test para crear tu archivo .env
   ```ssh
    DEBUG=True
    SECRET_KEY='11111111111818181818181811111111'
    ALLOWED_HOSTS=*
    CORS_ORIGIN_WHITELIST=http://localhost:3000,http://localhost:8000,http://localhost:8080
    
    
    DB_USER=
    DB_PASSWORD=
    DB_HOST=127.0.0.1
    DB_PORT=5432
    DB_NAME=paycode-db
    DB_ENGINE=django.db.backends.postgresql_psycopg2

   ```
   `NOTA: Usa tu usuario y contraseña de postgres`
4. En la misma carpeta ejecuta las migraciones

   ```ssh
   python manage.py makemigrations;
   python manage.py migrate
   ```
5. Ahora instala los fixtures para el dummy data

   ```ssh
   python .\manage.py loaddata .\fixtures\data.json
   ```
   
6. Inicia el servidor

   ```ssh
    python .\manage.py runserver
    ```
   
   
### Info del proyecto

Este proyecto fue desarrollado basado en una practica la cuál es generar contratos para el backend y front end los cuales
pérmitan de manera sencilla la integración de los servicios y la comunicación entre los mismos.

Se generó un documento contratos_sprint.md el cual contiene los contratos de los servicios que se implementaron en el proyecto.
También se generó un diagrama entidad relación en el archivo diagrama ER.png
El proyecto cuenta con dos usuarios cargados en los fixtures.
Los usuarios tienen dos perfiles, super_administrator y administrator.

- **super_administrator** : Puede crear, editar y eliminar clientes y pagos de clientes
- **administrator** : Solo puede ver los clientes y pagos de clientes

Las credenciales de cada uno son las siguientes:

- **super_administrator** :
  - email: dj-superadmin@paycode.io 
  - password: admin123
- **administrator** :
  - email: dj-admin@paycode.io
  - password: admin123


La api está documentada en el url:

http://localhost:8000/api/swagger/

usa el servicio de token/ para obtener el token de autenticación y usa el token en el Authorize con la palabra Bearer antes del token.

`EJEMPLO: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY5ODQ4MDQwLCJpYXQiOjE2Njk4NDc3NDAsImp0aSI6IjQwYTQ0MGRkYTk1MjRjYTliYmRlNTUwODMzZjYwMGQwIiwidXNlcl9pZCI6MX0.11mvl3StKfxX0hwKVHXzgSdlI0TUN7kJEEVPeaeLdYg`

### Ejecutar pruebas

Para ejecutar las pruebas unitarias ejecuta el siguiente comando

```ssh
python .\manage.py test
```





