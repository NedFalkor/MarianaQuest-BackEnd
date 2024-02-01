from django.urls import path, include
from rest_framework.routers import DefaultRouter

from MQ_users.viewsets.auth_user_viewset import AuthUserViewSet
from MQ_users.viewsets.dive_group_viewset import DiveGroupViewSet
from MQ_users.viewsets.diver_profile_viewset import DiverProfileViewSet
from MQ_users.viewsets.register_user_viewset import RegisterUserViewSet

router = DefaultRouter()
router.register(r'users', RegisterUserViewSet, basename='users')
router.register(r'auth', AuthUserViewSet, basename='auth')
router.register(r'diver-profiles', DiverProfileViewSet, basename='diver-profiles')
router.register(r'dive-groups', DiveGroupViewSet, basename='dive-groups')

# Custom URL patterns if needed
register_user_urlpatterns = [
    path('register/', RegisterUserViewSet.as_view({'post': 'create'}), name='register'),
]

auth_user_urlpatterns = [
    path('login/', AuthUserViewSet.as_view({'post': 'login'}), name='auth-login'),
    path('logout/', AuthUserViewSet.as_view({'post': 'logout'}), name='auth-logout'),
    path('delete_account/', AuthUserViewSet.as_view({'delete': 'delete_account'}), name='auth-delete-account'),
]

# Including default router URLs and custom URLs
urlpatterns = router.urls + register_user_urlpatterns + auth_user_urlpatterns
