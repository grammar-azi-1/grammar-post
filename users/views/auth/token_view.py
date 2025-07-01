
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

__all__ = [
    "GenerateValidTokenAPIView",
]


class GenerateValidTokenAPIView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")

        if not user_id:
            return Response({"error": "user_id is required"}, status=400)

        payload = {
            "token_type": "access",
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(minutes=30),
            "iat": datetime.utcnow(),
            "jti": "manual-token"
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        return Response({"token": token})