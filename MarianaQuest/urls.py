from django.urls import path, include
from rest_framework.routers import DefaultRouter

from MQ_users.viewsets.RegisterUserViewSet import RegisterUserViewSet

router = DefaultRouter()
router.register(r'users', RegisterUserViewSet, basename='registered')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.jwt')),
]
