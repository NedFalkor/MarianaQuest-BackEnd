from django import forms
from django.core.exceptions import ValidationError
from MQ_users.models.custom_user import CustomUser


class CustomUserCheck(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Un utilisateur avec cet e-mail existe déjà.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and CustomUser.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Un utilisateur avec ce nom d'utilisateur existe déjà.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        # Autres validations personnalisées si nécessaire
        return cleaned_data
