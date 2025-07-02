from django.urls import path
from account.views import *

urlpatterns = [
    # Verfication endpoints
    path(
        "users/send-verification-code/", 
        SendVerificationCodeView.as_view(), 
        name="send_verification_code"
    ),
]