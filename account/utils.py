from django.utils.timezone import now
from datetime import timedelta    


def is_online(self, timeout_seconds=5):
    return self.last_active >= now() - timedelta(seconds=timeout_seconds)