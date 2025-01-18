from django.apps import AppConfig


class AccountingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accountings'

    def ready(self):
        import apps.accountings.signals
