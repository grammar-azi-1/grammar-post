#!/bin/sh

echo "🛠 Making migrations for all apps..."
python manage.py makemigrations

echo "🛠 Applying all migrations..."
python manage.py migrate --noinput

echo "👤 Creating superuser if not exists..."
python manage.py create_super_user

echo "🚀 Starting Celery worker in background..."
celery -A grammar worker --loglevel=info &

echo "🌐 Starting Django server..."
python daphne grammar.asgi:application
