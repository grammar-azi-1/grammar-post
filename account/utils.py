from django.utils.timezone import now
from datetime import timedelta

def is_online(user, threshold_seconds=3):
    """
    İstifadəçinin son aktivliyi müəyyən saniyələr içindədirsə, online sayılır.
    """
    return user.last_active and (now() - user.last_active).total_seconds() <= threshold_seconds