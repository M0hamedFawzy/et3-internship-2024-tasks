#!/bin/sh
echo "Waiting for postgres..."

while ! nc -z $SQL_HOST 5432; do
  sleep 0.1
done

python3 manage.py test