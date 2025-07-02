from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
    )
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView
from account.api.serializers import UserAPIProfileSerializer, UserTokenRefreshSerializer, UserOnlineSerizalizer, UsersMainProfileSerizalizer, GroupSerizalizer, UserRoleSerializer
from account.api.filters import UserFilterset
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
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
    serializer_class = UserOnlineSerizalizer

    def get_queryset(self):
        threshold = now() - timedelta(seconds=3)
        online_users = User.objects.filter(last_active__gte=threshold)
        return online_users


class UserRetrieveUpdateView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UsersMainProfileSerizalizer


class UserListCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsersMainProfileSerizalizer
    filterset_class = UserFilterset


class GroupListCreateAPIView(ListCreateAPIView):
    serializer_class = GroupSerizalizer
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
