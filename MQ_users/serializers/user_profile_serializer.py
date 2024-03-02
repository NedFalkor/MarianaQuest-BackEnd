from rest_framework import serializers
from MQ_users.models.custom_user import CustomUser
from MQ_users.validators.custom_user_validator import CustomUserValidator


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']

    def validate(self, data):
        # Création d'une instance de formulaire pour la validation
        if self.instance:
            form = CustomUserValidator(data, instance=self.instance)
        else:
            form = CustomUserValidator(data)

        # Vérification de la validité du formulaire
        if form.is_valid():
            return form.cleaned_data
        else:
            raise serializers.ValidationError(form.errors)
