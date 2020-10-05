import socket
from logging import Logger
from smtplib import SMTPException
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.utils import timezone

from async_email.email import send_email
from async_email.task import BaseTask

logger: Logger = get_task_logger(__name__)


def send_email_task(
    context: Dict, to: Tuple[str], email_category: str, from_email: str = None
):
    logger.info(f"context: {context}")
    logger.info(f"to_email: {to}")

    send_email(
        to=to, email_category=email_category, from_email=from_email, context=context,
    )

    email_sent_at = timezone.now()
    return {"email_sent_at": email_sent_at}


def create_tasks_for_email_categories(categories: Union[Tuple, List]):
    """
    Create a new task for each email category on categories

    The task has the same name of the category. To call the task you can do:

    kwargs = {
        "email_category": "fake_category",
        "context": {},
        "to": "me@eltonplima.dev",
        "from_email": "contact@eltonplima.dev",
    }
    result = celery_app.send_task("fake_category", kwargs=kwargs,)
    """
    for category in categories:
        logger.info(f"registering task send_email for the queue: {category}")
        shared_task(
            send_email_task,
            queue=category,
            name=category,
            autoretry_for=(SMTPException, ConnectionRefusedError, socket.timeout),
            base=BaseTask,
        )


create_tasks_for_email_categories(settings.ASYNC_EMAIL_TEMPLATES.keys())
