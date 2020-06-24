from django.apps import AppConfig


class RseConfig(AppConfig):
    name = 'rse'

    def ready(self):
        import rse.auth
