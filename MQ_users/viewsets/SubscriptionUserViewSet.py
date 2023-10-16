from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login, logout
from MQ_users.serializers import SubscriptionUserSerializer


class SubscriptionUserViewSet(viewsets.ViewSet):
    serializer_class = SubscriptionUserSerializer

    def get_serializer(self, *args, **kwargs):
        return SubscriptionUserSerializer(*args, **kwargs)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
        if user:
            login(request, user)
            return Response({"message": "Connecté avec succès"}, status=status.HTTP_200_OK)
        return Response({"error": "Erreur de connexion"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def logout(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
