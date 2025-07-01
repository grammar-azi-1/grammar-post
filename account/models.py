from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta
# Create your models here.

class User(AbstractUser):
    phone = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    online_status = models.BooleanField(default=False)
    last_active = models.DateTimeField(default=now)

    def postCount(self):
        return len(self.posts.all()
)
