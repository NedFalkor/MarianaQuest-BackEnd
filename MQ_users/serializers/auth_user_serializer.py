from django.contrib.auth import authenticate
from rest_framework import serializers


class AuthUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')
        password = attrs.get('password')

        if email:
            user = authenticate(email=email, password=password)
        elif username:
            user = authenticate(username=username, password=password)
        else:
            raise serializers.ValidationError("Email ou Username doit être renseigné")

        if not user:
            raise serializers.ValidationError("Impossible de ce connecter avec ces identifiants")

        attrs['user'] = user
        return attrs
