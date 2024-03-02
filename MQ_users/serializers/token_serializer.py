from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Custom serializer to refresh access tokens.
    """

    def validate(self, attrs):
        data = super().validate(attrs)

        # You can add custom validation logic here if needed.

        return data
