from django.urls import path
from account.views import *
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    # Auth endpoints
    path(
        "users/register/", 
        RegisterView.as_view(),
        name="register"
    ),

    path(
        "users/login/", 
        LoginView.as_view(), 
        name="login"
    ),

    path(
        "users/logout/", 
        LogoutView.as_view(), 
        name="logout"
    ),

    path(
        "token/", 
        CustomTokenObtainPairView.as_view(), 
        name="token_obtain_pair"
    ),
    
    path(
        "token/refresh/", 
        TokenRefreshView.as_view(), 
        name="token_refresh"
    ),
]