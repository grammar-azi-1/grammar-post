import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Query string-dən JWT tokenini əldə et
        query_string = self.scope['query_string'].decode()
        token = None
        for param in query_string.split('&'):
            if param.startswith('token='):
                token = param.split('=')[1]
                break

        if not token:
            await self.close()
            return

        # İstifadəçini autentifikasiya et
        user = await self.get_user_from_token(token)
        if not user:
            await self.close()
            return

        self.user = user
        self.user_group = f"user_{user.id}"

        # İstifadəçini qrupa əlavə et
        await self.channel_layer.group_add(
            self.user_group,
            self.channel_name
        )
        await self.accept()

        # Bağlantı təsdiqi göndər
        await self.send(text_data=json.dumps({
            "message": f"WebSocket istifadəçi {user.id} üçün qoşuldu"
        }))

    async def disconnect(self, close_code):
        if hasattr(self, 'user_group'):
            await self.channel_layer.group_discard(
                self.user_group,
                self.channel_name
            )

    async def receive(self, text_data):
        # Müştəridən gələn mesajları idarə et (lazım gələrsə)
        data = json.loads(text_data)
        await self.send(text_data=json.dumps({
            "message": "Qəbul edildi",
            "data": data
        }))

    async def send_notification(self, event):
        # Bildirişi müştəriyə göndər
        await self.send(text_data=json.dumps({
            "type": "notification",
            "data": event["data"]
        }))

    @database_sync_to_async
    def get_user_from_token(self, token):
        try:
            from rest_framework_simplejwt.tokens import AccessToken
            from django.contrib.auth import get_user_model
            User = get_user_model()
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            return User.objects.get(id=user_id)
        except Exception:
            return None


class OnlineUserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("online_users_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("online_users_group", self.channel_name)

    async def broadcast_online(self, event):
        await self.send(text_data=json.dumps({
            "type": "user_online",
            "message": event.get("message", ""),
        }))