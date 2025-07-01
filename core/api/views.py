from rest_framework.generics import ListCreateAPIView
from core.models import Check_up
from core.api.serializers import CheckUpSerializer
from django.conf import settings
from django.http import JsonResponse
import requests

Url = settings.BOT_URL
my_token = settings.BOT_TOKEN
my_chatid = settings.CHAT_ID

def send_file_to_telegram(file_field, bot_token, chat_id):
    url = f'https://api.telegram.org/bot{bot_token}/sendDocument'

    # file_field should be a File object (e.g., from a model like checkup.file)
    with file_field.open('rb') as f:
        files = {
            'document': (file_field.name, f)
        }
        data = {
            'chat_id': chat_id
        }
        response = requests.post(url, files=files, data=data)
        return response.json()

class CheckUpApiView(ListCreateAPIView):
    serializer_class = CheckUpSerializer
    queryset = Check_up.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            checkup = Check_up.objects.create(**validated_data)
            # Optionally modify or inspect validated_data
            message = f'comment:{checkup.comment},\nphone_number:{checkup.phone_number}'
            file = f'file:{checkup.file.file}'
            url = f'https://api.telegram.org/bot{my_token}/sendMessage?chat_id={my_chatid}&text={message}'
            Fileurl = f'https://api.telegram.org/bot{my_token}/sendDocument?chat_id={my_chatid}&document={file}'

            if checkup.accept_policy:
                serializer.save()
                send_file_to_telegram(checkup.file, my_token, my_chatid)
                requests.get(url)
                return JsonResponse(data=serializer.data, safe=False, status=201)
            return JsonResponse(data=serializer.errors, safe=False, status=400)