from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from MQ_users.models.dive_group import DiveGroup
from MQ_users.serializers.dive_group_serializers import DiveGroupSerializer


class DiveGroupViewSet(viewsets.ModelViewSet):
    queryset = DiveGroup.objects.all()
    serializer_class = DiveGroupSerializer

    def perform_create(self, serializer):
        self.validate_divers(serializer.validated_data)
        serializer.save()

    def perform_update(self, serializer):
        self.validate_divers(serializer.validated_data)
        serializer.save()

    def validate_divers(self, data):
        # Validation pour s'assurer que chaque formateur a entre 1 et 2 plongeurs
        for trainer_field in ['trainer_one', 'trainer_two']:
            trainer = data.get(trainer_field)
            if trainer:
                diver_count = len(data['divers'])
                if diver_count < 1 or diver_count > 2:
                    raise ValidationError(f"{trainer.username} doit avoir entre 1 et 2 plongeurs.")
