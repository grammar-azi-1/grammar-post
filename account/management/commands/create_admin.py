from django.core.management import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='superadmin').exists():
            User.objects.create_superuser("superadmin", 'admin@test.com', 'admin')
            self.stdout.write(self.style.SUCCESS('Succesfully created super user!'))
        else:
            self.stdout.write(self.style.ERROR('Cant create another user with the same name!'))
