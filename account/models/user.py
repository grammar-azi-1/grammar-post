# account/models/user.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from account.managers import CustomUserManager
from utils.slug_manager import generate_unique_slug


class CustomUser(AbstractUser):
    """
    Custom user model that uses email as the unique identifier, 
    and also uses a unique username for profile display.
    """

    username = models.CharField(
        max_length=150,
        unique=True,           
    )
    email = models.EmailField(
        _("email address"),
        unique=True            
    )
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True
    )
    bio = models.TextField(
        blank=True,
        null=True
    )
    slug = models.SlugField(
        unique=True,
        blank=True
    )
    is_verified = models.BooleanField(
        default=False
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.slug:
            base = self.username or self.email.split("@")[0]
            self.slug = generate_unique_slug(base, CustomUser)
        super().save(*args, **kwargs)