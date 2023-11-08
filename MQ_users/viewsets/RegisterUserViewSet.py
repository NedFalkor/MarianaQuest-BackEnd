from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from MQ_users.models import CustomUser
from MQ_users.serializers import RegisterUserSerializer


class RegisterUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]

    @classmethod
    def get_extra_actions(cls):
        return []

    def create(self, request, *args, **kwargs):
        # Retrieve email or username from the request data
        email_or_username = request.data.get('email_or_username')
        role = request.data.get('role', 'PLONGEUR')  # Default to 'PLONGEUR' if not provided

        # Validate email_or_username is provided
        if not email_or_username:
            return Response({"error": "L'email ou le nom d'utilisateur est requis"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the email or username already exists
        if "@" in email_or_username and "." in email_or_username:
            if CustomUser.objects.filter(email=email_or_username).exists():
                return Response({"error": "L'email existe déjà"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if CustomUser.objects.filter(username=email_or_username).exists():
                return Response({"error": "Le nom d'utilisateur existe déjà"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the role is valid
        if role not in [choice[0] for choice in CustomUser.ROLE_CHOICES]:
            return Response({"error": "Le rôle fourni est invalide"}, status=status.HTTP_400_BAD_REQUEST)

        # If everything is okay, proceed to create the user
        response = super(RegisterUserViewSet, self).create(request, *args, **kwargs)
        return response
