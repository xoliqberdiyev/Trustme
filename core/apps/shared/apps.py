from django.apps import AppConfig


class SharedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.apps.shared'

    def ready(self):
        import core.apps.shared.admins.folder