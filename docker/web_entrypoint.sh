#!/bin/bash

# migrate possible changes
python manage.py migrate

python manage.py collectstatic --no-input

# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn core.wsgi:application \
    --name core \
    --bind 0.0.0.0:8080 \
    --workers 3 \
    --timeout 300 \
    "$@"
