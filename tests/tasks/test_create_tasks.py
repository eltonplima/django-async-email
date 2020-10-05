import socket
from smtplib import SMTPException
from unittest.mock import call

from async_email.task import BaseTask
from async_email.tasks import create_tasks_for_email_categories
from async_email.tasks import send_email_task


def test(mocker, settings):
    shared_task_mocked = mocker.patch("async_email.tasks.shared_task")

    categories = settings.ASYNC_EMAIL_TEMPLATES.keys()
    create_tasks_for_email_categories(categories=categories)

    calls = []

    for category in categories:
        calls.append(
            call(
                send_email_task,
                queue=category,
                name=category,
                autoretry_for=(SMTPException, ConnectionRefusedError, socket.timeout),
                base=BaseTask,
            )
        )

    shared_task_mocked.assert_has_calls(calls)
