import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

User = get_user_model()


def get_user_from_jwt(token):
    """
    Decodes the given JWT token and retrieves the corresponding user from the local database.
    Does not send any external HTTP request.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SIMPLE_JWT['SIGNING_KEY'],
            algorithms=[settings.SIMPLE_JWT['ALGORITHM']]
        )

        user_id = payload.get('user_id')
        if not user_id:
            raise AuthenticationFailed("Invalid token: no user ID.")

        user = User.objects.get(id=user_id)

        return {
            "id": user.id,
            "email": user.email,
            "full_name": str(user),  
        }

    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Token has expired.")
    except jwt.InvalidTokenError:
        raise AuthenticationFailed("Invalid token.")
    except User.DoesNotExist:
        raise AuthenticationFailed("User not found.")