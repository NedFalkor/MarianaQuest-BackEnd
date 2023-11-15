from django.urls import path, include
from rest_framework.routers import DefaultRouter

from MQ_users.viewsets.auth_user_viewset import AuthUserViewSet
from MQ_users.viewsets.diver_profile_viewset import DiverProfileViewSet
from MQ_users.viewsets.register_user_viewset import RegisterUserViewSet

router = DefaultRouter()
router.register(r'users', RegisterUserViewSet, basename='users')
router.register(r'auth', AuthUserViewSet, basename='auth')
router.register(r'diver-profiles', DiverProfileViewSet, basename='diver-profiles')

# Your custom route (if needed)
register_user_urlpatterns = [
    path('register/', RegisterUserViewSet.as_view({'post': 'create'}), name='register'),
]

urlpatterns = [
    path('', include(router.urls)),  # This includes routes for the viewsets
    path('', include(register_user_urlpatterns)),  # Your custom registration route (if needed)
]
