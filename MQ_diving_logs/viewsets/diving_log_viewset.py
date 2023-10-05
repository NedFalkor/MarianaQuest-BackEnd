from rest_framework import viewsets
from .models.diving_log import DivingLog
from .serializers.diving_log_serializer import DivingLogSerializer


class DivingLogViewSet(viewsets.ModelViewSet):
    queryset = DivingLog.objects.all()
    serializer_class = DivingLogSerializer
