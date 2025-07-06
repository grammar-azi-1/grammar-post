from django.db.models.signals import post_save
from blog.models import Post
from django.dispatch import receiver

@receiver(post_save, sender=Post)
def get_tags(sender, instance, created, **kwargs):
    if created:
        instance.tags = [word for word in instance.content.split() if word.startswith('#')]
        instance.save()
