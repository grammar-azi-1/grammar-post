from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView
from account.api.serializers import (
    UserAPIProfileSerializer,
    UserTokenRefreshSerializer,
    UserOnlineSerizalizer,
    UsersMainProfileSerizalizer,
    GroupSerizalizer,
    UserRoleSerializer
)
from account.api.filters import UserFilterset
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.utils.timezone import now, timedelta
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

User = get_user_model()


class PingView(APIView):
    """
    Ping endpoint to update user's last active time.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Ping user activity",
        responses={200: openapi.Response("Pong", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'status': openapi.Schema(type=openapi.TYPE_STRING, example="ping")
            }
        ))}
    )
    def get(self, request):
        request.user.last_active = now()
        request.user.save(update_fields=['last_active'])
        return Response({'status': 'ping'})


class UserTokenObtainPairView(TokenObtainPairView):
    """
    Obtain JWT access and refresh tokens.
    """

    @swagger_auto_schema(
        operation_summary="Obtain JWT tokens",
        responses={200: openapi.Response(description="JWT access and refresh tokens", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access': openapi.Schema(type=openapi.TYPE_STRING),
                'refresh': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ))}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserTokenRefreshView(TokenRefreshView):
    """
    Refresh JWT access token using the refresh token.
    """

    @swagger_auto_schema(
        operation_summary="Refresh JWT token",
        responses={200: openapi.Response(description="New JWT access token", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ))}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserOnlineApiView(ListAPIView):
    """
    List users who were active within the last 3 seconds.
    """
    serializer_class = UserOnlineSerizalizer

    def get_queryset(self):
        threshold = now() - timedelta(seconds=3)
        return User.objects.filter(last_active__gte=threshold)

    @swagger_auto_schema(operation_summary="List online users")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserRetrieveUpdateView(RetrieveAPIView):
    """
    Retrieve a user's profile by ID.
    """
    queryset = User.objects.all()
    serializer_class = UsersMainProfileSerizalizer

    @swagger_auto_schema(operation_summary="Retrieve user profile by ID")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserListCreateView(ListCreateAPIView):
    """
    List all users or create a new user.
    """
    queryset = User.objects.all()
    serializer_class = UsersMainProfileSerizalizer
    filterset_class = UserFilterset

    @swagger_auto_schema(operation_summary="List all users")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Create a new user")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class GroupListCreateAPIView(ListCreateAPIView):
    """
    List and create user groups.
    """
    serializer_class = GroupSerizalizer
    queryset = Group.objects.all()

    @swagger_auto_schema(operation_summary="List all groups")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Create a new group")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserRoleListCreateAPIView(ListCreateAPIView):
    """
    Admin only: Assign a group/role to a user.
    """
    serializer_class = UserRoleSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(operation_summary="Assign role to user")
    def post(self, request, *args, **kwargs):
        serializer = UserRoleSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {
            "postId": serializer.instance.id,
            "message": "Role assigned successfully",
            "role": [group.name for group in serializer.instance.groups.all()],
        }

        return JsonResponse(response, safe=False, status=201)
