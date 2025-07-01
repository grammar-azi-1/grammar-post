from django.utils.timezone import now
from django.utils.deprecation import MiddlewareMixin

class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and (now() - request.user.last_active).seconds > 5:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            User.objects.filter(pk=request.user.pk).update(last_active=now())
        return self.get_response(request)
    

class UpdateLastOwnActivityMiddleware(MiddlewareMixin):

    def procces_request(self, request):

        if request.user.is_authenticated:
            request.user.last_active = now()
            request.user.save()