# API DyP

Este proyecto implementa una API REST con arquitectura hexagonal, siguiendo las mejores prácticas de desarrollo basado en pruebas unitarias (TDD) y pruebas de comportamiento (BDD). 

## Características principales

- **Base de Datos:** PostgreSQL con soporte para PostGIS.
- **Arquitectura:** Hexagonal.
- **Pruebas:** Desarrollo basado en pruebas unitarias y de comportamiento.
- **Integración:** Documentación generada automáticamente con Swagger.

## Repositorio

Clona el repositorio utilizando el siguiente comando:

```bash
git clone https://github.com/AdminDyP/kuspit-payroll-system-back.git
```
## Requisitos Previos

Asegúrate de tener los siguientes componentes instalados en tu sistema:

- **Python 3.10+**
- **PostgreSQL 13+**
- **Docker y Docker Compose**
- **Virtualenv** (opcional)
- **Redis** para la gestión de tareas en segundo plano.

Para entornos de desarrollo:

- **Linux/Mac:** Preinstalado con muchas distribuciones modernas.
- **Windows:** Utiliza `choco` para instalar herramientas adicionales, como Make y Redis (instrucciones detalladas más adelante).

## Configuración del Entorno Local

1. **Crear y activar un entorno virtual**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
2. **Instalar dependencias del proyecto**:   
   ```bash
   pip install -r requirements.txt
   ```
3. **Configurar el archivo .env**:

En la carpeta raíz del proyecto, crea un archivo .env con el siguiente contenido:
   ```bash
   
   DEBUG=True
   SECRET_KEY='TuClaveSecreta'
   ALLOWED_HOSTS=*
   CORS_ORIGIN_WHITELIST=http://localhost:3000,http://localhost:8000,http://localhost:8080
   
   # Base de Datos
   DB_USER=postgres
   DB_PASSWORD=1234
   DB_HOST=127.0.0.1
   DB_PORT=5432
   DB_NAME=dyp-db
   DB_ENGINE=django.contrib.gis.db.backends.postgis
   
   # Redis y Celery
   REDIS_URL=redis://127.0.0.1:6379/0
   CELERY_BROKER_URL=redis://127.0.0.1:6379/0
   CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
   ```
Nota: Ajusta los valores según tu configuración local o de Docker.

## Inicialización de la Base de Datos

1. **Crear la base de datos en PostgreSQL**:

2. **Conéctate a PostgreSQL y ejecuta**:

   ```sql
   CREATE DATABASE "dyp-db";
   ```
3. **Ejecutar migraciones**:
```bash
python manage.py makemigrations
python manage.py migrate
   ```
4. **Cargar datos de prueba (fixtures)**:
```bash
python manage.py loaddata fixtures/data.json
   ```
5. **Iniciar el servidor**:
```bash
python manage.py runserver
   ```
Accede a la API en http://localhost:8000.

## Desplegar el Proyecto con Docker

1. **Construir la imagen del proyecto**:

   ```bash
   docker compose build
   ```
2. **Levantar los contenedores**:

   ```bash
   docker compose up -d
      ```
3. **Configurar PostGIS en la base de datos**:

Accede al contenedor de PostgreSQL:
```bash
docker exec -it <id_container_db> bash
```
Instala PostGIS:
```bash
apt-get update && apt-get install -y postgis
```
Crea la extensión:
```bash
CREATE EXTENSION postgis;
```
4. **Ejecutar migraciones en el contenedor de la API**:

```bash
docker exec -it <id_container_api> bash
python manage.py makemigrations
python manage.py migrate
```