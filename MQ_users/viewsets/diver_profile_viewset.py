from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

from MQ_users.models.diver_profile import DiverProfile
from MQ_users.permissions.is_owner_or_admin_permission import IsOwnerOrAdmin
from MQ_users.serializers.diver_profile_serializer import DiverProfileSerializer


class DiverProfileViewSet(viewsets.ModelViewSet):
    queryset = DiverProfile.objects.all()
    serializer_class = DiverProfileSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_permissions(self):
        """
        Instance et renvoie la liste des permissions que ce viewset nécessite.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    # Create
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Read
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # Update
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
