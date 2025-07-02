import logging
from rest_framework.views import APIView, Response, status
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from account.serializers.auth import RegisterSerializer

__all__ = ["RegisterView"]

logger = logging.getLogger(__name__)

User = get_user_model()


class RegisterView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        operation_summary="User Registration",
        operation_description="""
        Register a new user with email, password, and personal details.  
        Accepts `multipart/form-data` content type for potential file uploads such as profile image.
        """,
        consumes=["multipart/form-data"],
        responses={
            201: openapi.Response(
                description="User registered successfully",
                examples={
                    "application/json": {
                        "message": "Registration successful."
                    }
                }
            ),
            400: openapi.Response(
                description="Registration failed due to validation errors",
                examples={
                    "application/json": {
                        "email": ["This field is required."],
                        "password": ["This field may not be blank."]
                    }
                }
            )
        },
        tags=["Authentication"]
    )
    def post(self, request):
        logger.info(
            "Registration request received with data: %s", 
            request.data
        )

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            logger.info("Registration successful for user: %s", user.email)
            return Response(
                {"message": "Registration successful."},
                status=status.HTTP_201_CREATED
            )

        logger.warning("Registration failed: %s", serializer.errors)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )