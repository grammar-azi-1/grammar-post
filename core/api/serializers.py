from rest_framework import serializers
from core.models import Check_up

class CheckUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check_up
        fields = (
            'file',
            'comment',
            'phone_number',
            'accept_policy',
        )
