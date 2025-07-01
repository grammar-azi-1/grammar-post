from blog.api.views import CommentCreateAPIView, PostCreateAPIView, PostDeleteAPIView, PostRetrieveUpdateAPIView, PostShareRetrieveUpdateAPIView, NotificationsAPIView, NotificationRetrieveAPIView
from django.urls import path

urlpatterns = [
    path('comments/<int:post_id>/', CommentCreateAPIView.as_view(), name='comments'),
    path('posts/', PostCreateAPIView.as_view(), name='posts'),
    path('admin/post/<int:pk>/', PostDeleteAPIView.as_view(), name='post_destroy'),
    path('posts/<int:pk>/', PostRetrieveUpdateAPIView.as_view(), name='post_update'),
    path('posts/<int:pk>/share', PostShareRetrieveUpdateAPIView.as_view(), name='post_share'),
    path('notifications/<int:userId>/', NotificationsAPIView.as_view(), name='notifications'),
    path('notifications/<int:pk>/', NotificationRetrieveAPIView.as_view(), name='notification_delete'),
]