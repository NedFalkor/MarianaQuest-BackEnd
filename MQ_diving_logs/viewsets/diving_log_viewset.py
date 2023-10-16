from rest_framework import viewsets, status
from rest_framework.response import Response
from MQ_diving_logs.models.diving_log import DivingLog
from MQ_diving_logs.serializers.diving_log_serializer import DivingLogSerializer


class DivingLogViewSet(viewsets.ModelViewSet):
    queryset = DivingLog.objects.all()
    serializer_class = DivingLogSerializer

    def create(self, request, *args, **kwargs):
        """Customize the creation of a diving log."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """Customize the update of a diving log."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Customize the deletion of a diving log."""
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        """Customize the listing of diving logs."""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """Customize the retrieval of a specific diving log."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
