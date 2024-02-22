import json

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
        data = request.data.copy()
        print("Request Data:", data)

        diver_profile_data_json = data.get('diverProfileData')
        if diver_profile_data_json:
            diver_profile_data = json.loads(diver_profile_data_json)
            print("Parsed Diver Profile Data:", diver_profile_data)
        else:
            return Response({"error": "Missing diverProfileData"}, status=status.HTTP_400_BAD_REQUEST)

        emergency_contact_data = diver_profile_data.pop('emergency_contact', None)
        identity_photo = data.get('identity_photo')

        # Serialize and save DiverProfile
        serializer = DiverProfileSerializer(data=diver_profile_data)
        if serializer.is_valid():
            print("Validated Data: ", serializer.validated_data)
            diver_profile = serializer.save(identity_photo=identity_photo)

            if not serializer.is_valid():
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Serialize and save EmergencyContact
            if emergency_contact_data:
                emergency_contact_serializer = EmergencyContactSerializer(data=emergency_contact_data)
                if emergency_contact_serializer.is_valid():
                    EmergencyContact.objects.create(diver_profile=diver_profile,
                                                    **emergency_contact_serializer.validated_data)
                else:
                    diver_profile.delete()  # Rollback if EmergencyContact is invalid
                    return Response(emergency_contact_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
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

            serializer.save()

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
