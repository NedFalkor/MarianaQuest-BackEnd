from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/', include('MQ_users.urls')),
                  path('api/auth/', include('dj_rest_auth.urls')),
                  path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('', include('MQ_diving_logs.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
