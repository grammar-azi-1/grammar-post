import requests
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

def get_user_form_jwt (token):
    """
    user-service-dən istifadəçi məlumatlarını əldə edir.
    """
    headers = {
        'Authorization': f'Bearer {token}'
    }
    try:
        response = requests.get(
            'https://user-service-grammar-azi.onrender.com/api/v1/users/me/',
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise AuthenticationFailed(f"İstifadəçi məlumatlarını əldə etmək mümkün olmadı: {str(e)}")