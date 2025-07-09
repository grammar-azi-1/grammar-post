from django.utils.timezone import now

class UpdateLastActivityMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response 

    def _is_token_auth(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', '')
        return auth.startswith('Bearer ') or auth.startswith('Token ')

    def __call__(self, request):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = getattr(request, 'user', None)

        if user and user.is_authenticated and self._is_token_auth(request):
            User.objects.filter(pk=user.pk).update(last_active=now())

        return self.get_response(request) 
