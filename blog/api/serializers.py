from rest_framework import serializers
from blog.models import Comment, Post
from blog.models import Notification



class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
       model = Notification
       fields = (
            "id",
            "type",
            "postId",
            "commentId",
            "created_date",
       )
       
class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = (
            'id',
            'parentCommentId',
            'userId',
            'postId',
            'content',
            'image',
            'like',
            'created_date',
        )

class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = (
            'id',
            'userId',
            'image',
            'content',
        )

class PostFilterSerializer(serializers.ModelSerializer):
    shareLink = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id',
            'tags',
            'image',
            'content',
            'like',
            'title',
            'comment_count',
            'created_date',
            'shareLink',
            'userId',
        )

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        
        return None

    def get_shareLink(self, obj):
        return f'https://grammarazi.onrender.com/en/api/posts/{obj.id}/'

class PostShareSerializer(serializers.ModelSerializer):
    
    message = serializers.SerializerMethodField()
    shareLink = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'message',
            'shareLink',
        )

    
    def get_message(self, obj):
        return "Link kopyalandı"
    
    def get_shareLink(self, obj):
        return f'https://grammarazi.onrender.com/en/api/posts/{obj.id}/'