#!/bin/sh
echo "Waiting for postgres..."

while ! nc -z postgres-internship2024-kalimatcash 5432; do
  sleep 0.1
done

echo "PostgreSQL started"
python3 manage.py makemigrations --noinput
python3 manage.py migrate
python3 manage.py collectstatic --noinput
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@domain.com', 'P@ssw0rd')" | python3 manage.py shell
gunicorn --config gunicorn-cfg.py project.wsgi