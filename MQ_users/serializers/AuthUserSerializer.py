from django.contrib.auth import authenticate
from rest_framework import serializers


class AuthUserSerializer(serializers.Serializer):
    emailOrUsername = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        # Tentez d'authentifier par e-mail
        user = authenticate(email=attrs['emailOrUsername'], password=attrs['password'])

        # Si l'authentification par e-mail échoue, essayez par nom d'utilisateur
        if not user:
            user = authenticate(username=attrs['emailOrUsername'], password=attrs['password'])

        if not user:
            raise serializers.ValidationError("Les informations d'identification fournies sont incorrectes.")

        return attrs
