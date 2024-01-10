from django import forms
from django.core.exceptions import ValidationError
from MQ_users.models import DiverProfile, CustomUser


class DiverProfileCheck(forms.ModelForm):
    class Meta:
        model = DiverProfile
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get('user')
        identity_photo = cleaned_data.get('identity_photo')

        # Validation pour s'assurer que l'utilisateur a le rôle 'DIVER'
        if user and user.role != 'DIVER':
            raise ValidationError("Le profil doit être associé à un utilisateur avec le rôle 'DIVER'.")

        # Valider que la photo d'identité est présente pour les profils complets
        if not identity_photo:
            raise ValidationError("Une photo d'identité est requise pour le profil du plongeur.")

        return cleaned_data
