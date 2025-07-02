import logging
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from drf_yasg import openapi

from account.models import CustomUser
from account.serializers import UserSerializer, UpdateProfileSerializer


__all__ = [
    "UserProfileView",
    "UpdateProfileView"
]

# Set up logging
logger = logging.getLogger(__name__)


class UserProfileView(APIView):
    """
    API view to retrieve the authenticated user's profile.

    This view is accessible only to authenticated users. It returns the profile
    data of the user based on their JWT authentication token.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Profile"],
        operation_summary="Get your own profile",
        operation_description="Returns the profile information of the currently authenticated user.",
        responses={
            200: openapi.Response(
                description="User profile retrieved successfully",
                schema=UserSerializer
            ),
            401: openapi.Response(description="Authentication credentials were not provided or invalid")
        }
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UpdateProfileView(APIView):
    """
    View for updating a user's profile with support for multipart form data.
    
    This view allows users to update their first name, last name, bio, and profile picture.
    It supports multipart form data format (image uploads).
    """

    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser] 

    @swagger_auto_schema(
        tags=["Profile"],
        operation_summary="Update user profile",
        operation_description="Allows the authenticated user to update their profile information such as name, bio, and profile picture.",
        request_body=UpdateProfileSerializer,
        responses={
            200: openapi.Response(
                description="Profile updated successfully",
                schema=UpdateProfileSerializer,
            ),
            400: openapi.Response(
                description="Invalid input or failed validation"
            ),
        }
    )
    def put(self, request, *args, **kwargs):
        """
        Updates the user profile with the provided data.
        
        Only the authenticated user can update their own profile.
        """
        user = request.user  
        
        # Deserialize the incoming request data using the UpdateProfileSerializer
        serializer = UpdateProfileSerializer(
            user, data=request.data
        )
        
        # Validate the data
        if serializer.is_valid():
            # Save the updated profile
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Return validation errors if any
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )