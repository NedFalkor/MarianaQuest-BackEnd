from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from MQ_users.models.dive_group import DiveGroup
from MQ_users.serializers.dive_group_serializer import DiveGroupSerializer


class DiveGroupViewSet(viewsets.ModelViewSet):
    queryset = DiveGroup.objects.all()
    serializer_class = DiveGroupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        instance = serializer.save()
        divers = serializer.validated_data.get('divers')
        instance.divers.set(divers)

    def perform_update(self, serializer):
        instance = serializer.save()
        self.set_divers(serializer, instance)

    def set_divers(self, serializer, instance):
        divers = serializer.validated_data.get('divers')
        if divers:
            instance.divers.set(divers)
            instance.save()

    def validate_divers(self, data):
        # Validation pour s'assurer que le boat_driver est un formateur
        boat_driver = data.get('boat_driver')
        if boat_driver and boat_driver.role != 'INSTRUCTOR':
            raise ValidationError("Le conducteur du bateau doit être un formateur.")

        # Validation pour s'assurer que les formateurs ont entre 1 et 2 plongeurs
        divers = data.get('divers', [])
        for trainer_field in ['trainer_one', 'trainer_two']:
            trainer = data.get(trainer_field)
            if trainer and trainer.role != 'INSTRUCTOR':
                raise ValidationError(f"{trainer.username} doit être un formateur.")

            diver_count = len(divers) if isinstance(divers, list) else divers.filter(role='DIVER').count()
            if diver_count < 1 or diver_count > 2:
                raise ValidationError(f"{trainer.username} doit avoir entre 1 et 2 plongeurs.")