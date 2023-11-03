from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets.RegisterUserViewSet import RegisterUserViewSet
from .viewsets.AuthUserViewSet import AuthUserViewSet

router = DefaultRouter()
router.register(r'users', RegisterUserViewSet, basename='registered')
router.register(r'auth', AuthUserViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.jwt')),
]
