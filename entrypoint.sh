#!/bin/bash
set -e

echo "Booting TaskMates Application..."

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
