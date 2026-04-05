#!/bin/bash
set -e

# If DATABASE_URL is not set, we're likely in local docker-compose
if [ -z "$DATABASE_URL" ]; then
  echo "Waiting for local postgres (db container)..."
  while ! nc -z db 5432 2>/dev/null; do
    sleep 0.5
  done
  echo "PostgreSQL started"
else
  echo "External DATABASE_URL detected, skipping local DB wait..."
fi

# Apply database migrations
echo "Make migrations"
python manage.py makemigrations users services customers servicers chatbot
echo "Apply database migrations"
python manage.py migrate

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput   

# Execute the passed command (e.g., gunicorn)
exec "$@"
