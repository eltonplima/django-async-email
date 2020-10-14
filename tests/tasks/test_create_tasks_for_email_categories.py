import socket
from smtplib import SMTPException
from unittest.mock import call

from async_email.task import BaseTask
from async_email.tasks import create_tasks_for_email_categories
from async_email.tasks import generate_task_qualified_name
from async_email.tasks import generate_task_queue_qualified_name
from async_email.tasks import send_template_email_task


def test(mocker, settings):
    shared_task_mocked = mocker.patch("async_email.tasks.shared_task")

    categories = settings.ASYNC_EMAIL_TEMPLATES.keys()
    create_tasks_for_email_categories(categories=categories)

    calls = []

    for category in categories:
        task_name = f"async_email.tasks.{category}"
        task_queue_name = task_name
        calls.append(
            call(
                send_template_email_task,
                queue=task_queue_name,
                name=task_name,
                autoretry_for=(SMTPException, ConnectionRefusedError, socket.timeout),
                base=BaseTask,
            )
        )

    shared_task_mocked.assert_has_calls(calls)


def test_generate_task_qualified_name():
    assert generate_task_qualified_name("taskX") == "async_email.tasks.taskX"


def test_generate_task_queue_qualified_name():
    assert generate_task_queue_qualified_name("taskX") == "async_email.tasks.taskX"
