#!/bin/bash

echo "Starting development environment..."

# Change to the core directory where manage.py is located
cd /app/core

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput --verbosity 0

# Create superuser if it doesn't exist
python manage.py createsuperuser --noinput || true

# Start development server
echo "Django development server is running!"
echo "Access your application at: http://localhost:8000"
echo "Or use: http://127.0.0.1:8000"
echo ""
python manage.py runserver 0.0.0.0:8000 