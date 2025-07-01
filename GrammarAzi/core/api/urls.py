from django.urls import path
from core.api.views import CheckUpApiView

urlpatterns = [
    path('checkups/', CheckUpApiView.as_view(), name = 'checkups')
]