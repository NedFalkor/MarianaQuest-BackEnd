from django import forms
from django.core.exceptions import ValidationError
from MQ_users.models.dive_group import DiveGroup
from datetime import datetime


class DiveGroupValidator(forms.ModelForm):
    class Meta:
        model = DiveGroup
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        boat_driver = cleaned_data.get('boat_driver')
        trainer_one = cleaned_data.get('trainer_one')
        trainer_two = cleaned_data.get('trainer_two')
        divers = cleaned_data.get('divers')
        created_on = cleaned_data.get('created_on')

        if boat_driver and boat_driver.role != 'INSTRUCTOR':
            raise ValidationError("Le conducteur du bateau doit être un instructeur.")

        for trainer in [trainer_one, trainer_two]:
            if trainer:
                diver_count = len(divers) if isinstance(divers, list) else divers.filter(role='DIVER').count()
                if diver_count < 1 or diver_count > 2:
                    raise ValidationError(f"{trainer.username} doit avoir entre 1 et 2 plongeurs.")

        if trainer_one and trainer_two and trainer_one == trainer_two:
            raise ValidationError("Les deux entraîneurs ne peuvent pas être la même personne.")

        max_divers = 10
        if divers and len(divers) > max_divers:
            raise ValidationError(f"Le nombre de plongeurs ne doit pas dépasser {max_divers}.")

        all_divers_in_groups = set()
        for group in DiveGroup.objects.all():
            for diver in group.divers.all():
                if diver in all_divers_in_groups:
                    raise ValidationError(f"Le plongeur {diver.username} est déjà inscrit dans un autre groupe.")
                all_divers_in_groups.add(diver)

        if created_on and created_on > datetime.now():
            raise ValidationError("La date de création ne peut pas être postérieure.")

        return cleaned_data
