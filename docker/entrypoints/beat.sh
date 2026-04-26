#!/bin/sh

set -e

echo "Starting Celery beat..."

celery -A infrastructure.celery.celery_app beat \
  --loglevel=info