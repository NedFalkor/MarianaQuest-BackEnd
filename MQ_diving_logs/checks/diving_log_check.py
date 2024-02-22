from django import forms
from datetime import date, datetime

from MQ_diving_logs.models.diving_log import DivingLog
from MQ_users.models.dive_group import DiveGroup


class DivingLogCheck(forms.ModelForm):
    class Meta:
        model = DivingLog
        fields = '__all__'

    def clean_dive_group(self):
        dive_group = self.cleaned_data.get('dive_group')
        if dive_group and not DiveGroup.objects.filter(id=dive_group.id).exists():
            raise forms.ValidationError("Le groupe choisi n'existe pas")
        return dive_group

    def clean_dive_date(self):
        dive_date = self.cleaned_data.get('dive_date')
        if dive_date and dive_date > date.today():
            raise forms.ValidationError("La date ne peut pas être dans le futur")
        return dive_date

    def clean_depth(self):
        depth = self.cleaned_data.get('depth')
        if depth is not None and depth < 0:
            raise forms.ValidationError("La profondeur ne peut pas être négative")
        return depth

    def clean_duration_dive(self):
        duration = self.cleaned_data.get('duration_dive')
        if duration is not None and duration <= 0:
            raise forms.ValidationError("La durée doit être positive")
        return duration

    def clean_temperatures(self):
        # Extracted logic to a separate function for clarity
        air_temp = self.cleaned_data.get('air_temperature')
        water_temp = self.cleaned_data.get('water_temperature')
        if air_temp and water_temp and water_temp > air_temp:
            self.add_error('water_temperature', "La température de l'eau ne peut pas être au dessus de la "
                                                "température de l'air")

    def clean_surface_return_vs_duration(self):
        duration = self.cleaned_data.get('duration_dive')
        surface_return = self.cleaned_data.get('surface_return')
        try:
            if surface_return:
                surface_return_time = datetime.strptime(surface_return, '%H:%M')
                surface_return_minutes = surface_return_time.hour * 60 + surface_return_time.minute
                if duration and surface_return_minutes > duration:
                    self.add_error('surface_return', "Le temps de retour à la surface ne peut pas dépasser "
                                                     "la durée")
        except ValueError:
            self.add_error('surface_return', "Format de temps invalide")

    def clean_consumption_values(self):
        consumption_start = self.cleaned_data.get('consumption_start')
        consumption_end = self.cleaned_data.get('consumption_end')
        if consumption_start and consumption_end and consumption_start <= consumption_end:
            self.add_error('consumption_end', "La consommation finale doit être inférieure à celle du début")

    def clean_visibility_vs_weather(self):
        weather = self.cleaned_data.get('weather')
        current = self.cleaned_data.get('current')
        visibility = self.cleaned_data.get('visibility')
        if weather == 'downpour' and visibility == 'good':
            self.add_error('visibility', "La bonne visibilité est impossible lors d'une averse")
        if current == 'strong' and visibility == 'good':
            self.add_error('visibility', "La bonne visibilité est impossible lors de forts courants")

    def clean(self):
        cleaned_data = super().clean()
        self.clean_temperatures()
        self.clean_surface_return_vs_duration()
        self.clean_consumption_values()
        self.clean_visibility_vs_weather()
        return cleaned_data
