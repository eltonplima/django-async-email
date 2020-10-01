import socket
from logging import Logger
from smtplib import SMTPException
from typing import Dict, Tuple

from async_email.email import send_email
from async_email.task import BaseTask
from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.utils import timezone

logger: Logger = get_task_logger(__name__)


@shared_task(
    autoretry_for=(SMTPException, ConnectionRefusedError, socket.timeout),
    queue="send_email",
    base=BaseTask,
)
def send_email_task(
    context: Dict, to: Tuple[str], email_category: str, from_email: str = None
):
    logger.info(f"context: {context}")
    logger.info(f"to_email: {to}")
    if isinstance(to, str):
        to = (to,)
    else:
        to = tuple(to)

    from_email = from_email or settings.DEFAULT_FROM_EMAIL
    send_email(
        to=to, email_category=email_category, from_email=from_email, context=context,
    )

    email_sent_at = timezone.now()
    return {"email_sent_at": email_sent_at}


def route_task(name, args, kwargs, options, task=None, **kw):
    if name == "myapp.tasks.compress_video":
        return {
            "exchange": "video",
            "exchange_type": "topic",
            "routing_key": "video.compress",
        }
    else:
        return {"queue": "celery"}
