from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from MQ_users.models import CustomUser
from MQ_users.serializers.register_user_serializer import RegisterUserSerializer


class RegisterUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        role = serializer.validated_data.get('role', 'PLONGEUR')

        # Check if the email or username already exists
        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "L'email existe déjà"}, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(username=username).exists():
            return Response({"error": "Le nom d'utilisateur existe déjà"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the role is valid
        if role not in [choice[0] for choice in CustomUser.ROLE_CHOICES]:
            return Response({"error": "Le rôle fourni est invalide"}, status=status.HTTP_400_BAD_REQUEST)

        # If everything is okay, proceed to create the user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @classmethod
    def get_extra_actions(cls):
        return []
