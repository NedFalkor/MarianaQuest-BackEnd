from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # ... vos autres modèles d'URL si vous en avez
    path('admin/', admin.site.urls),
    path('', include('MQ_users.urls')),  # Redirigez la racine vers les URLs de MQ_users
    path('', include('MQ_diving_logs.urls')),  # Redirigez également la racine vers les URLs de MQ_diving_logs
]
