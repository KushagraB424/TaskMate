#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

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
