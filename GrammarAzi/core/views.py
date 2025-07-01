from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _ 
from django.urls import reverse_lazy
from django.views.generic import FormView
from core.forms import CheckUpForm
from django.core.exceptions import ValidationError
from core.models import Check_up
from django.conf import settings
import requests
from django.contrib import messages

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
# Create your views here.

class Home(FormView):
    form_class = CheckUpForm
    template_name = 'home.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            checkup = form.save(False)
            checkup.phone_number = '+994' + checkup.phone_number
            messages.add_message(self.request, messages.SUCCESS, "Successfully sent!!!")
            message = f'comment:{checkup.comment},\n phone_number:{checkup.phone_number}'
            file = f'file:{checkup.file.file}'
            url = f'https://api.telegram.org/bot{my_token}/sendMessage?chat_id={my_chatid}&text={message}'
            Fileurl = f'https://api.telegram.org/bot{my_token}/sendDocument?chat_id={my_chatid}&document={file}'

            if checkup.accept_policy:
                form.save()
                send_file_to_telegram(checkup.file, my_token, my_chatid)
                requests.get(Fileurl)
                requests.get(url)
            else:
                raise ValidationError('accept_policy must be True!(error 400)')
            return redirect(reverse_lazy('home'))
        return self.form_invalid(form)