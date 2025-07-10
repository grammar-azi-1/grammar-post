from django.utils.timezone import now

class UpdateLastActivityMiddleware:

    def __init__(self, get_response):
        self.response = get_response

    def __call__(self, request):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = getattr(request, 'user', None)

        if user and user.is_authenticated:
            User.objects.filter(pk=request.user.pk).update(last_active=now())

        return self.response(request)
    