#!/bin/bash
set -e

if [ "$RENDER" != "true" ]; then
  echo "Waiting for local postgres..."
  while ! nc -z db 5432; do
    sleep 0.1
  done
  echo "PostgreSQL started"
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
