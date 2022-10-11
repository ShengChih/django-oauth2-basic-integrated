from rest_framework import serializers
from social_auth.providers.google.constants \
    import (
        PROVIDER_NAME as GOOGLE_PROVIDER_NAME
    )


class ExchangeProviderSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    provider_name = serializers.CharField(required=True)


class ExchangeGoogleSerializer(ExchangeProviderSerializer):
    id_token = serializers.CharField(required=True)
    access_token = serializers.CharField(required=True)

    def load_provider_utils(self):
        from social_auth.providers.google import utils
        return utils

    def validate_provider_name(self, value):
        if GOOGLE_PROVIDER_NAME == value:
            return value

        raise serializers.ValidationError("Provider Name is invalid")

    def validate(self, data):
        super(ExchangeGoogleSerializer, self).validate(data)
        self.utils = self.load_provider_utils()
        return data

    def verify_token(self):
        return self.utils.verify_id_token(
            self.validated_data.get('email'),
            self.validated_data.get('id_token')
        )

    def login_user(self):
        if not self.verify_token():
            raise Exception("Google ID token is invalid")

        user = self.utils.login_user(
            self.validated_data.get('email'),
            self.validated_data.get('access_token')
        )

        if not user:
            raise Exception("User not found")

        return user

        


PROVIDER_SERIALIERS = {
    GOOGLE_PROVIDER_NAME: ExchangeGoogleSerializer
}
