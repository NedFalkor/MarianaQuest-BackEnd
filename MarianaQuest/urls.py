from django.urls import path
from MQ_users.viewsets.RegisterUserViewSet import RegisterUser

urlpatterns = [
    # ... your other url patterns
    path('register/', RegisterUser.as_view(), name='register_user'),
]
