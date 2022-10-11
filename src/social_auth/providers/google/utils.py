from social_auth.providers.google.constants import (
    GET_PROFILE_API,
)
from datetime import datetime
import requests


def get_user_profile(access_token):
    request = requests.get(
        GET_PROFILE_API,
        params={"access_token": access_token, "alt": "json"},
    )
    request.raise_for_status()
    return request.json()


def init_profile_to_user(user_profile):
    return {
        'first_name': user_profile.get('given_name') or '',
        'last_name': user_profile.get('family_name') or '',
        'username': user_profile.get('name') or '',
        'is_superuser': False,
        'is_staff': False,
        'is_active': True,
        'date_joined': datetime.now()
    }
