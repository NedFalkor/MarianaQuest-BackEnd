from django.urls import path, include
from rest_framework.routers import DefaultRouter
from MQ_users.viewsets.register_user_viewset import RegisterUserViewSet
from MQ_users.viewsets.auth_user_viewset import AuthUserViewSet
from MQ_diving_logs.viewsets.diving_log_viewset import DivingLogViewSet  # Assurez-vous d'importer le viewset correct

router_users = DefaultRouter()
router_users.register(r'users', RegisterUserViewSet, basename='registered')
router_users.register(r'auth', AuthUserViewSet, basename='auth')

router_diving_logs = DefaultRouter()
router_diving_logs.register(r'diving-logs', DivingLogViewSet, basename='diving-log')

urlpatterns = [
    path('', include(router_users.urls)),
    path('auth/', include('djoser.urls.jwt')),
    path('api/', include(router_diving_logs.urls)),
]
