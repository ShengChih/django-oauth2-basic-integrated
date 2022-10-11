from django.contrib.auth import get_user_model
from social_auth.providers.google.constants import (
    VERIFY_TOKEN_API,
    GET_PROFILE_API,
)
from datetime import datetime
import requests
import string
import secrets


def get_secret_random_string(length):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))


def get_user_profile(access_token):
    return requests.get(
        GET_PROFILE_API,
        params={"access_token": access_token, "alt": "json"},
    ).json()


def verify_id_token(email, id_token):
    ret = requests.get(
        VERIFY_TOKEN_API,
        params={"id_token": id_token}
    ).json()

    if 'error' in ret:
        return False

    return email == ret["email"]


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


def login_user(email, access_token):
    user = None
    user_profile = None

    try:
        user_profile = get_user_profile(access_token)

        if email != user_profile['email']:
            raise Exception("User Email doesn't match")

        User = get_user_model()
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        is_created, user = User.object.update_or_create(
            email=email,
            defaults=init_profile_to_user(user_profile)
        )
        user.set_password(get_secret_random_string(10))
        user.save()

    if not user.is_active:
        return None

    user.last_login = datetime.now()
    user.save()

    return user
