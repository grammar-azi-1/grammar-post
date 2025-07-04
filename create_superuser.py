from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Creates a superuser if it does not exist using environment variables'

    def handle(self, *args, **options):
        User = get_user_model()

        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "adminpass")
        username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superuser with email \"{email}\" created."))
        else:
            self.stdout.write(self.style.WARNING(f"Superuser with email \"{email}\" already exists."))
