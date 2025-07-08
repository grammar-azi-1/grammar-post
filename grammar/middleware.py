from django.utils.timezone import now

class UpdateLastActivityMixin:
    def initial(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            User.objects.filter(pk=request.user.pk).update(last_active=now())
        return super().dispatch(request, *args, **kwargs)