# account/serializers/user/user.py
from rest_framework import serializers
from account.models.user import CustomUser
from typing import Any, Dict


class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email", 
            "username",   
            "bio", 
            "profile_picture", 
            "slug"
        ]

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return obj.profile_picture.url 
        return None

 
class UpdateProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["username", "bio", "profile_picture"]

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return obj.profile_picture.url
        return None

    def update(self, instance: CustomUser, validated_data: Dict[str, Any]) -> CustomUser:
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
