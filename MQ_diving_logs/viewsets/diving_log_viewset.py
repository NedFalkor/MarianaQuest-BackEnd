from rest_framework import viewsets, status
from rest_framework.response import Response
from MQ_diving_logs.models.diving_log import DivingLog
from MQ_diving_logs.serializers.diving_log_serializer import DivingLogSerializer


class DivingLogViewSet(viewsets.ModelViewSet):
    queryset = DivingLog.objects.all()
    serializer_class = DivingLogSerializer

    def create(self, request, *args, **kwargs):
        request.data['status'] = 'EN_ATTENTE'

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        user = request.user

        if hasattr(user, 'role') and user.role == 'FORMATEUR':
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)

        # Si ce n'est pas un formateur ou si la validation échoue, refuser
        return Response(status=status.HTTP_403_FORBIDDEN, data={"message": "Permission refusée."})

    def destroy(self, request, *args, **kwargs):
        user = request.user

        if hasattr(user, 'role') and user.role == 'FORMATEUR':
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_403_FORBIDDEN, data={"message": "Permission refusée."})

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
