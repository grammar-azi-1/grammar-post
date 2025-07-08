from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework import serializers
from blog.api.serializers import PostSerializer
from django.contrib.auth.models import Group, Permission
from account.utils import is_online
from blog.models import Notification

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = (
            'id',
            'name',
        )


class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer

    class Meta:
       model = Group
       fields = (
            'name',
            'permissions',
       )


class UserOnlineSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    online_status = serializers.SerializerMethodField()
    last_active = serializers.SerializerMethodField()

    class Meta:
        model=User
        fields=(
            'id',
            'username',
            'profile_picture',
            'post_count',
            'online_status',
            'last_active',
            'groups'
        )

    def get_last_active(self, obj):
        return obj.last_active

    def get_post_count(self, obj):
        return obj.postCount() if hasattr(obj, 'postCount') else 0

    def get_online_status(self, obj):
        request = self.context.get('request')
        request.user.online_status = is_online(obj)

        return is_online(obj)


class UsersMainProfileSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True)
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'profile_picture',
            'posts'
        )


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'groups',
        )


class UserAPIProfileSerializer(serializers.ModelSerializer):

    refresh = serializers.CharField()
    access = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'refresh',
            'access',
            'id',
            'username',
            'password',
        )


class UserTokenRefreshSerializer(serializers.ModelSerializer):

    access = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'access',
        )


class UserTokenPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        user_serializer = UserProfileSerializer(self.user)
        data.update(user_serializer.data)
        return data
    

class UserRoleSerializer(serializers.ModelSerializer):

    groups = GroupSerializer(many=True)
    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = (
            'id',
            'groups',
        )

class NotificationSerializer(serializers.ModelSerializer):

    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    recipient = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
       model = Notification
       fields = (
            "id",
            "type",
            'sender',
            'recipient',
            "postId",
            "commentId",
            "created_date",
       )