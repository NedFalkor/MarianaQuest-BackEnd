from rest_framework import serializers

from MQ_users.models.dive_group import DiveGroup
from MQ_users.models import CustomUser
from MQ_users.validators.dive_group_validator import DiveGroupValidator


class DiveGroupSerializer(serializers.ModelSerializer):
    divers = serializers.PrimaryKeyRelatedField(
        many=True, queryset=CustomUser.objects.filter(role='DIVER')
    )

    class Meta:
        model = DiveGroup
        fields = '__all__'

    def validate(self, data):
        # Créer une instance de DiveGroupCheck avec les données
        form = DiveGroupValidator(data)

        # Exécuter la validation
        if form.is_valid():
            return form.cleaned_data
        else:
            raise serializers.ValidationError(form.errors)
