from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/websocket_path/", consumers.MyConsumer.as_asgi()),
]