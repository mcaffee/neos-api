from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        super().ready()
        from core.injector import configure_injector
        configure_injector()
