from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from MQ_users.models import CustomUser
from MQ_users.serializers.RegisterUserSerializer import RegisterUserSerializer


class RegisterUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]

    @classmethod
    def get_extra_actions(cls):
        return []

    def create(self, request, *args, **kwargs):
        email_or_username = request.data.get('email_or_username')

        if "@" in email_or_username and "." in email_or_username:
            if CustomUser.objects.filter(email=email_or_username).exists():
                return Response({"error": "L'email existe déjà"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if CustomUser.objects.filter(username=email_or_username).exists():
                return Response({"error": "Le nom d'utilisateur existe déjà"}, status=status.HTTP_400_BAD_REQUEST)

        response = super(RegisterUserViewSet, self).create(request, *args, **kwargs)
        return response
