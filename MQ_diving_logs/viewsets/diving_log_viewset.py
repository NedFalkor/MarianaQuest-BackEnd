from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from MQ_diving_logs.models.diving_log import DivingLog
from MQ_diving_logs.permissions.is_diver_permission import IsDiver
from MQ_diving_logs.serializers.diving_log_serializer import DivingLogSerializer


class DivingLogViewSet(viewsets.ModelViewSet):
    queryset = DivingLog.objects.all()
    serializer_class = DivingLogSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated(), IsDiver()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        # Lors de la création, le statut est automatiquement mis à 'EN_ATTENTE'
        request.data['status'] = 'AWAITING'
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()

        # Seul un formateur peut changer le statut d'un DivingLog
        if hasattr(user, 'role') and user.role != 'INSTRUCTOR':
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={"message": "Only instructors can modify status"})

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = request.user

        # Seul un formateur peut supprimer un DivingLog
        if hasattr(user, 'role') and user.role != 'INSTRUCTOR':
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={"message": "Only instructors can delete a log"})

        return super().destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
