from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from MQ_users.models import CustomUser
from MQ_users.serializers.RegisterUserSerializer import RegisterUserSerializer


class RegisterUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        return super(RegisterUserViewSet, self).create(request, *args, **kwargs)
