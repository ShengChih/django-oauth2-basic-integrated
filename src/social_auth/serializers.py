from django.contrib.auth import get_user_model

from rest_framework import serializers
from social_auth.providers.google.constants import (
    PROVIDER_NAME as GOOGLE_PROVIDER_NAME
)
from social_auth.providers.facebook.constants import (
    PROVIDER_NAME as FACEBOOK_PROVIDER_NAME
)
from libs.random.generators import get_secret_random_string

from datetime import datetime


class ExchangeProviderSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    provider_name = serializers.CharField(required=True)
    access_token = serializers.CharField(required=True)

    def validate(self, data):
        super(ExchangeProviderSerializer, self).validate(data)
        self.utils = self.load_provider_utils()
        return data

    def login_user_with_token(self):
        user = None
        user_profile = None
        User = get_user_model()

        try:
            email = self.validated_data.get('email')
            user_profile = self.utils.get_user_profile(self.validated_data.get('access_token'))

            if email != user_profile['email']:
                raise Exception("User Email doesn't match")

            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user, is_created = User.object.update_or_create(
                email=email,
                defaults=self.utils.init_profile_to_user(user_profile)
            )
            user.set_password(get_secret_random_string(10))
            user.save()
        except Exception:
            user = None
            return user

        if user and not user.is_active:
            return None

        user.last_login = datetime.now()
        user.save()

        return user


class ExchangeGoogleSerializer(ExchangeProviderSerializer):
    def load_provider_utils(self):
        from social_auth.providers.google import utils
        return utils

    def validate_provider_name(self, value):
        if GOOGLE_PROVIDER_NAME == value:
            return value

        raise serializers.ValidationError("Provider Name is invalid")


class ExchangeFacebookSerializer(ExchangeProviderSerializer):
    def load_provider_utils(self):
        from social_auth.providers.facebook import utils
        return utils

    def validate_provider_name(self, value):
        if FACEBOOK_PROVIDER_NAME == value:
            return value

        raise serializers.ValidationError("Provider Name is invalid")


PROVIDER_SERIALIERS = {
    GOOGLE_PROVIDER_NAME: ExchangeGoogleSerializer,
    FACEBOOK_PROVIDER_NAME: ExchangeFacebookSerializer
}
