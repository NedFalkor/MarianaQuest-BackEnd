from rest_framework import serializers
from .models import User

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'confirm_password']

    def validate(self, data):
        # Vérifiez que les deux mots de passe correspondent
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Les mots de passe ne correspondent pas."})
        return data

    def create(self, validated_data):
        # Supprimez le champ de confirmation du mot de passe car il n'est pas nécessaire pour la création du modèle
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(**validated_data)
        return user
