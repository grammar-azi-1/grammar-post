#!/bin/sh

echo "🛠 Making migrations for all apps..."
python manage.py makemigrations

echo "🛠 Applying all migrations..."
python manage.py migrate --noinput

echo "🚀 Starting Celery worker in background..."
celery -A grammar worker --loglevel=info &

echo "🌐 Starting Django server..."
python manage.py runserver 0.0.0.0:8000
