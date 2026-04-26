#!/bin/sh

set -e

echo "Waiting for database..."

while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
  sleep 1
done

echo "Database available - running migrations"

python manage.py migrate --noinput

echo "Starting Django ASGI server"

gunicorn config.asgi:application \
  -k uvicorn.workers.UvicornWorker \
  -b 0.0.0.0:8000 \
  --workers 2 \
  --timeout 60