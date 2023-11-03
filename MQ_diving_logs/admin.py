from django.contrib import admin

from MQ_diving_logs.models.diving_log import DivingLog

# Enregistrez le modèle DivingLog dans l'admin
admin.site.register(DivingLog)
