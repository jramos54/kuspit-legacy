#!/bin/bash

# Espera hasta que Redis esté listo
echo "Esperando a que Redis esté listo..."
until nc -z -v -w30 redis 6379
do
  echo "Redis aún no está listo. Esperando 5 segundos..."
  sleep 5
done

echo "Redis está listo. Iniciando la aplicación..."
exec "$@"
