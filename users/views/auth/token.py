from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers.auth.token import CustomTokenObtainPairSerializer

__all__ = [
    "CustomTokenObtainPairView",
]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

