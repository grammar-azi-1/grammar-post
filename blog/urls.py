from django.urls import path
from blog.views import BlogView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('blog/', login_required(BlogView.as_view(), login_url='login'), name='blog')
]
