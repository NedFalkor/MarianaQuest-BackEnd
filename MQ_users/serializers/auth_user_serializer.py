from django.contrib.auth import authenticate
from rest_framework import serializers

from MQ_users.validators.custom_user_validator import CustomUserValidator


class AuthUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')
        password = attrs.get('password')

        user_data = {'email': email, 'username': username}
        user_validator = CustomUserValidator(data=user_data)

        if not user_validator.is_valid():
            raise serializers.ValidationError(user_validator.errors)

        if email:
            user = authenticate(email=email, password=password)
        elif username:
            user = authenticate(username=username, password=password)
        else:
            raise serializers.ValidationError("Email or username must be provided.")

        if not user:
            raise serializers.ValidationError("Unable to log in with provided credentials.")

        attrs['user'] = user
        return attrs
