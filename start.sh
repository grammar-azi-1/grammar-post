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
<<<<<<< HEAD
daphne grammar.asgi:application

=======
exec daphne -b 0.0.0.0 -p ${PORT:-8000} grammar.asgi:application
>>>>>>> a5ca55e73b852f17cd1f6735feae8396aae9e6f5

