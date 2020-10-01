from django.apps import AppConfig


class AsyncEmailConfig(AppConfig):
    name = "async_email"

    def ready(self):
        pass
