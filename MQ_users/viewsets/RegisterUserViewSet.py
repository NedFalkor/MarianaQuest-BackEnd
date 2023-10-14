from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from MQ_users.models import CustomUser

class RegisterUser(APIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        username = request.data.get('username')

        # Vérifiez si l'email est déjà pris
        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

