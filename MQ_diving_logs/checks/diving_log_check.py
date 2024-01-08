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
            raise forms.ValidationError("Selected dive group does not exist.")
        return dive_group

    def clean_dive_date(self):
        dive_date = self.cleaned_data.get('dive_date')
        if dive_date and dive_date > date.today():
            raise forms.ValidationError("Dive date cannot be in the future.")
        return dive_date

    def clean_depth(self):
        depth = self.cleaned_data.get('depth')
        if depth is not None and depth < 0:
            raise forms.ValidationError("Depth cannot be negative.")
        return depth

    def clean_duration_dive(self):
        duration = self.cleaned_data.get('duration_dive')
        if duration is not None and duration <= 0:
            raise forms.ValidationError("Dive duration must be positive.")
        return duration

    def clean_temperatures(self):
        # Extracted logic to a separate function for clarity
        air_temp = self.cleaned_data.get('air_temperature')
        water_temp = self.cleaned_data.get('water_temperature')
        if air_temp and water_temp and water_temp > air_temp:
            self.add_error('water_temperature', "Water temperature cannot exceed air temperature.")

    def clean_surface_return_vs_duration(self):
        duration = self.cleaned_data.get('duration_dive')
        surface_return = self.cleaned_data.get('surface_return')
        # Ensure surface_return is a valid time string and convert it to minutes
        try:
            if surface_return:
                surface_return_time = datetime.strptime(surface_return, '%H:%M')
                surface_return_minutes = surface_return_time.hour * 60 + surface_return_time.minute
                if duration and surface_return_minutes > duration:
                    self.add_error('surface_return', "Surface return time cannot exceed dive duration.")
        except ValueError:
            self.add_error('surface_return', "Invalid time format for surface return.")

    def clean_consumption_values(self):
        consumption_start = self.cleaned_data.get('consumption_start')
        consumption_end = self.cleaned_data.get('consumption_end')
        if consumption_start and consumption_end and consumption_start <= consumption_end:
            self.add_error('consumption_end', "End consumption should be less than start consumption.")

    def clean_visibility_vs_weather(self):
        weather = self.cleaned_data.get('weather')
        current = self.cleaned_data.get('current')
        visibility = self.cleaned_data.get('visibility')
        if weather == 'downpour' and visibility == 'good':
            self.add_error('visibility', "Good visibility is unlikely during a downpour.")
        if current == 'strong' and visibility == 'good':
            self.add_error('visibility', "Good visibility is unlikely in strong currents.")

    def clean(self):
        cleaned_data = super().clean()
        self.clean_temperatures()  # Call the specific validation method for temperatures
        self.clean_surface_return_vs_duration()
        self.clean_consumption_values()
        self.clean_visibility_vs_weather()
        return cleaned_data
