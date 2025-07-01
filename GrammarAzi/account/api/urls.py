from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from account.api.views import PingView, UserTokenObtainPairView, UserTokenRefreshView, UserOnlineApiView, UserRetrieveUpdateView, GroupListCreateAPIView, UserListCreateView, UserRoleListCreateAPIView

urlpatterns = [
    path('token/', UserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', UserTokenRefreshView.as_view(), name='token_refresh'),
    path('users/<int:pk>/profile/', UserRetrieveUpdateView.as_view(), name='users_update'),
    path('users/', UserListCreateView.as_view(), name='users'),
    path('users/active/', UserOnlineApiView.as_view(), name='users_active'),
    path('groups/', GroupListCreateAPIView.as_view(), name='groups'),
    path('admin/assing-role/', UserRoleListCreateAPIView.as_view(), name='userroles'),
    path('ping/', PingView.as_view(), name='ping'),
]