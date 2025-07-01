from django.db import models
from core.models import AbstractModel
from django.contrib.auth import get_user_model
User = get_user_model()
from core.validators import validate_file_size
from blog.validators import validate_file_type

# Create your models here.

class Post(AbstractModel):
    userId = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    content = models.TextField(max_length=5000)
    like = models.PositiveIntegerField(default=0)
    tags = models.JSONField(default=list, blank=True, null=True)

    def len(self):
        return len(self.objects.all())
    
    def comment_count(self):
        return len(self.comments.all())

    def __str__(self):
        return self.title
    
class Comment(AbstractModel):
    parentCommentId = models.ForeignKey('self', related_name='child', on_delete=models.CASCADE, null=True, blank=True)
    userId = models.ForeignKey(User, related_name='comment_user', on_delete=models.CASCADE)
    postId = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, null=True, blank=True)

    like = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='comment_images/', blank=True, null=True, validators=[validate_file_size, validate_file_type])
    content = models.TextField(max_length=350)

    def len(self):
        return len(self.objects.all())

    def __str__(self):
        return self.content
    
class Notification(AbstractModel):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('reply', 'Reply'),
        ('comment_like', 'Like comment'),
        ('commented_comment', 'Commented to comment'),
    )
    recipient = models.ForeignKey(User, related_name='notification', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_notification', on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    postId = models.ForeignKey(Post, related_name='notification_post', on_delete=models.CASCADE, null=True, blank=True)
    commentId = models.ForeignKey(Comment, related_name='notification_comment', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.sender} {self.type}d to {self.recipient}'