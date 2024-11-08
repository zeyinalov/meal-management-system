#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Wait for the database to be ready
./wait-for-it.sh db:5432 --timeout=60 --strict -- echo "Database is up"

# Run database migrations
flask db upgrade

# Start Gunicorn
exec gunicorn wsgi:app -w 4 -b 0.0.0.0:5000