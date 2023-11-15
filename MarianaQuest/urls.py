from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('MQ_users.urls')),
    path('', include('MQ_diving_logs.urls')),
]