# Base image
FROM python:3.10-slim-buster

# Set work directory
# ADD ../.. /app
WORKDIR /app
COPY . /app/

# Set environment variables
ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    apt-get clean  && \
    apt install -y libpq-dev gdal-bin libgdal-dev && \
    apt-get install -y postgis && \
    apt-get install -y --no-install-recommends \
       postgresql postgis && \
    rm -rf /var/lib/apt/lists/*

# RUN apt-get update && apt-get install -y mlocate && updatedb

RUN export LD_LIBRARY_PATH=/usr/lib

# Install requirements
# RUN pip install geos
RUN pip install --upgrade pip && \
    pip install --no-cache-dir geos

RUN export GDAL_LIBRARY_PATH=$(locate libgdal.so)
RUN export GEOS_LIBRARY_PATH=$(locate libgeos_c.so)

RUN pip cache purge
RUN pip install --no-cache-dir -r requirements.txt

# Copia el script de espera y dale permisos de ejecución
COPY wait_for_redis.sh /wait_for_redis.sh
RUN chmod +x /wait_for_redis.sh

# Collect static
ENV DJANGO_SETTINGS_MODULE=configuracion.settings
COPY .env /app/.env
RUN python manage.py collectstatic --no-input

# Expose port 80 for the Django application
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", ":8000", "--workers", "4", "--threads" , "4" , "--timeout", "30", "configuracion.wsgi:application"]