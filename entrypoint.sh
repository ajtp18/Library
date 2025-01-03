#!/bin/sh

cd $(dirname $0)/libreria

gunicorn libreria.wsgi:application \
  --bind 0.0.0.0:${PORT:-8000} \
  --workers $(($(nproc) * 2 + 1)) \
  --threads 2 \
  --timeout 120 \
  --access-logfile '-' \
  --error-logfile '-' \
  --preload \
  --max-requests 150 \
  --max-requests-jitter 10
