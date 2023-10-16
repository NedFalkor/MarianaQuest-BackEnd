from django.contrib.auth import authenticate
from rest_framework import serializers


class SubscriptionUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        user = authenticate(email=attrs['email'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError("Les informations d'identification fournies sont incorrectes.")
        return attrs
