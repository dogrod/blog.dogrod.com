#!/bin/bash

# Collect static files
echo "Collect static files"
python3 manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python3 manage.py migrate --noinput

# Start server
echo "Starting server"
uwsgi --ini uwsgi.ini
