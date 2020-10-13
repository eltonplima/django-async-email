__all__ = ["send_email_template"]

from typing import Dict
from typing import Tuple

from celery import Celery
from celery.result import AsyncResult
from django.conf import settings


default_app_config = "async_email.apps.AsyncEmailConfig"


def send_email_template(
    to: Tuple[str], template_name: str, context: Dict, from_email: str = None
) -> AsyncResult:
    app = Celery("async_email", broker=settings.CELERY_BROKER_URL, backend="amqp")
    result = app.send_task(
        template_name,
        queue=template_name,
        kwargs={
            "template_name": template_name,
            "context": context,
            "to": to,
            "from_email": from_email or settings.DEFAULT_FROM_EMAIL,
        },
    )
    return result

