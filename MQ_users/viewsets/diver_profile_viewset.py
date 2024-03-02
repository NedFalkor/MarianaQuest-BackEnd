from rest_framework import viewsets, status, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response

from MQ_users.models import EmergencyContact
from MQ_users.models.diver_profile import DiverProfile
from MQ_users.permissions.is_owner_or_admin_permission import IsOwnerOrAdmin
from MQ_users.serializers.diver_profile_serializer import DiverProfileSerializer
from MQ_users.serializers.emergency_contact_serializer import EmergencyContactSerializer


class DiverProfileViewSet(viewsets.ModelViewSet):
    queryset = DiverProfile.objects.all()
    serializer_class = DiverProfileSerializer
    permission_classes = [IsOwnerOrAdmin]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    # Create
    def create(self, request, *args, **kwargs):
        # Pass 'request.data' which includes POST data and 'request.FILES' which includes file data
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            emergency_contact_data = serializer.validated_data.pop('emergency_contact', None)
            diver_profile = serializer.save()

            if emergency_contact_data:
                emergency_contact_serializer = EmergencyContactSerializer(data=emergency_contact_data)
                if emergency_contact_serializer.is_valid():
                    EmergencyContact.objects.create(diver_profile=diver_profile,
                                                    **emergency_contact_serializer.validated_data)
                else:
                    # If emergency contact is invalid, delete the diver profile and return the errors
                    diver_profile.delete()
                    return Response(emergency_contact_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # If everything is valid, return the created diver profile data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # If there are errors, return them
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
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            emergency_contact_data = serializer.validated_data.pop('emergency_contact', None)

            diver_profile = serializer.save()

            if emergency_contact_data:
                emergency_contact = instance.emergency_contact
                emergency_contact_serializer = EmergencyContactSerializer(emergency_contact,
                                                                          data=emergency_contact_data)
                if emergency_contact_serializer.is_valid():
                    emergency_contact_serializer.save()
                else:
                    return Response(emergency_contact_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
