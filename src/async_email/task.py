from abc import ABC

from celery import Task
from django.conf import settings


class BaseTask(Task, ABC):
    # https://docs.celeryproject.org/en/stable/userguide/tasks.html#Task.retry_backoff
    retry_backoff = True
    # https://docs.celeryproject.org/en/stable/userguide/tasks.html#Task.retry_backoff_max
    retry_backoff_max = 600
    # https://docs.celeryproject.org/en/stable/userguide/tasks.html#Task.retry_jitter
    retry_jitter = True
    # https://docs.celeryproject.org/en/stable/userguide/tasks.html#Task.time_limit
    time_limit = 60

    def retry(
        self,
        args=None,
        kwargs=None,
        exc=None,
        throw=True,
        eta=None,
        countdown=None,
        max_retries=None,
        **options,
    ):
        """
        Override the default implementation to allow us to customize the max_retries in runtime.
        """
        max_retries = settings.ASYNC_EMAIL_TASKS.get(self.name, {}).get(
            "max_retries", max_retries
        )

        return super().retry(
            args=args,
            kwargs=kwargs,
            exc=exc,
            throw=throw,
            eta=eta,
            countdown=countdown,
            max_retries=max_retries,
            **options,
        )
