from django.urls import path
from account.views import *

urlpatterns = [
    # User endpoints
    path(
        "users/me/", 
        UserProfileView.as_view(), 
        name="user-profile"
    ),

    path(
        "update-profile/", 
        UpdateProfileView.as_view(), 
        name="update-profile"
    ),

    path(
        "token/manual/", 
        GenerateValidTokenAPIView.as_view(), 
        name="manual-token"),
]