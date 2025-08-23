#!/bin/bash

echo "Starting production environment..."

# Change to the core directory where manage.py is located
cd /app/core

# Run migrations
python manage.py migrate

# Collect static files (commented out as requested)
python manage.py collectstatic --noinput

# Start production server with uvicorn
uvicorn core.asgi:application --host 0.0.0.0 --port 8000 