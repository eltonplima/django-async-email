from django.apps import AppConfig
from django.conf import settings
from kombu import Queue


class AsyncEmailConfig(AppConfig):
    name = "async_email"

    def ready(self):
        # Load the queues automatically
        CELERY_TASK_QUEUES = ()
        for queue_name in settings.ASYNC_EMAIL_TEMPLATES.keys():
            CELERY_TASK_QUEUES += (Queue(f"async_email.tasks.{queue_name}"),)
        settings.CELERY_TASK_QUEUES = CELERY_TASK_QUEUES
