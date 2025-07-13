from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
    )
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView
from account.api.serializers import UserAPIProfileSerializer, UserTokenRefreshSerializer, UserOnlineSerializer, UsersMainProfileSerializer, GroupSerializer, UserRoleSerializer
from account.api.filters import UserFilterset
from django.contrib.auth.models import Group
from datetime import timedelta
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.shortcuts import get_object_or_404
User = get_user_model()
from django.utils.timezone import now, timedelta
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

class PingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user.last_active = now()
        request.user.save(update_fields=['last_active'])
        return Response({'status': 'ping'})


class UserTokenObtainPairView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserOnlineApiView(ListAPIView):
    serializer_class = UserOnlineSerializer

    def get_queryset(self):
        threshold = now() - timedelta(seconds=31)
        queryset = User.objects.filter(last_active__gte=threshold)

        current_user = self.request.user

        if current_user.is_authenticated:
            # Update last_active
            current_user.last_active = now()
            current_user.save(update_fields=['last_active'])

            # Make sure they appear in the list
            if current_user not in queryset:
                queryset = queryset | User.objects.filter(pk=current_user.pk)

            # Send WebSocket update to clients
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "online_users_group",
                {
                    "type": "broadcast_online",
                    "message": f"{current_user.username} is active",
                }
            )

        return queryset.distinct()

class UserRetrieveUpdateView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UsersMainProfileSerializer


class UserListCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersMainProfileSerializer
    filterset_class = UserFilterset


class GroupListCreateAPIView(ListCreateAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    
class UserRoleListCreateAPIView(ListCreateAPIView):
    serializer_class = UserRoleSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser,]

    def post(self, request, *args, **kwargs):

        serializer = UserRoleSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {
            "postId": serializer.instance.id,
            "message": "Rol uğurla təyin olundu",
            "role": [group.name for group in serializer.instance.groups.all()],
        }

        return JsonResponse(response, safe=False, status=201)

        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)

        # response = {
        #     "postId": serializer.instance.id,
        #     "message": "Rol uğurla təyin olundu",
        #     "role": serializer.groups.name,
        # }
        
        # return JsonResponse(response, safe=False, status=201)
