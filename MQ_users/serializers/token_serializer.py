from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


class CustomTokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        return data
