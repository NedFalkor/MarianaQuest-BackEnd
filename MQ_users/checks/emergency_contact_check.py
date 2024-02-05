from django import forms
from django.core.exceptions import ValidationError
from MQ_users.models import EmergencyContact, DiverProfile


class EmergencyContactCheck(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        diver_profile = cleaned_data.get('diver_profile')
        landline = cleaned_data.get('landline')
        mobile = cleaned_data.get('mobile')
        email = cleaned_data.get('email')

        # Vérifiez si le contact d'urgence a au moins un moyen de contact
        if not (landline or mobile or email):
            raise ValidationError("Au moins un moyen de contact (téléphone fixe, mobile ou email) est requis.")

        # Vérifiez si le contact d'urgence est associé à un profil de plongeur
        if diver_profile and not DiverProfile.objects.filter(id=diver_profile.id).exists():
            raise ValidationError("Le profil de plongeur associé n'existe pas.")

        return cleaned_data
