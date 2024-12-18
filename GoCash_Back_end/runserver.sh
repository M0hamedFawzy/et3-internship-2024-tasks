#!/bin/sh

echo "Waiting for PostgreSQL to be ready..."

# Check for the postgres-gocash service at port 5432
while ! nc -z postgres-gocash 5432; do
  sleep 0.1
done

echo "PostgreSQL started."

# Run Django commands to prepare the app
python3 manage.py makemigrations --noinput
python3 manage.py migrate
python3 manage.py collectstatic --noinput

# Create an admin user if it doesn't already exist
echo "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'FAZZA', '106')
" | python3 manage.py shell

# Start Gunicorn with your GoCash project's WSGI
gunicorn --config gunicorn-cfg.py goCash.wsgi
