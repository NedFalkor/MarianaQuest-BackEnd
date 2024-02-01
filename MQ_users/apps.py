from django.apps import AppConfig


class MqUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MQ_users'

    def ready(self):
        from . import signals
        pass
