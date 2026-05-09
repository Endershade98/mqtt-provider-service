#!/bin/sh
set -e

echo "Starting Celery worker..."

celery -A infrastructure.celery.celery_app worker \
  --loglevel=info \
  --concurrency=4