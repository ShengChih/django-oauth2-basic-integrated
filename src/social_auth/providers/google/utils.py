from django.contrib.auth import get_user_model

from social_auth.providers.google.constants import (
    VERIFY_TOKEN_API,
    GET_PROFILE_API
)

import requests


def get_user_profile(access_token):
    return requests.get(
        GET_PROFILE_API,
        params={"access_token": access_token, "alt": "json"},
    )


def verify_id_token(email, id_token):
    ret = requests.get(
        VERIFY_TOKEN_API,
        params={"id_token": id_token}
    ).json()

    return email == ret["email"]


def get_user(email, access_token=None):
    user = None
    try:
        User = get_user_model()
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        if not access_token:
            return user

        user_profile = get_user_profile(access_token)

        if email != user_profile['email']:
            return user

        is_created, user = User.object.update_or_create(
            email=email,
            defaults={}
        )

    return user
