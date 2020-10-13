from datetime import datetime

import pytest
from freezegun import freeze_time

from async_email.tasks import send_template_email_task


def test_custom_from_email(context, mocker):
    send_email_mocked = mocker.patch("async_email.tasks.send_email_template")

    send_template_email_task(
        to=("noreply@example.com",),
        template_name="fake_category",
        context=context,
        from_email="fake_from@example.com",
    )
    send_email_mocked.assert_called_once_with(
        context=context,
        template_name="fake_category",
        from_email="fake_from@example.com",
        to=("noreply@example.com",),
    )


@freeze_time("2020-09-09")
def test_return(context, mocker):
    mocker.patch("async_email.tasks.send_email_template")

    result = send_template_email_task(
        to=("noreply@example.com",),
        template_name="fake_category",
        context=context,
        from_email="fake_from@example.com",
    )

    assert result == {"email_sent_at": datetime(2020, 9, 9)}


@pytest.mark.parametrize(
    "email,expected",
    [
        ("", ("",)),
        ("invalid", ("invalid",)),
        ("invalid-with-hyphen", ("invalid-with-hyphen",)),
        ("@invalid_email", ("@invalid_email",)),
        ("invalid_email@", ("invalid_email@",)),
        ("invalid_email@t.t", ("invalid_email@t.t",)),
        ("invalid_email@test.c", ("invalid_email@test.c",)),
        ("9invalid_email@test.c", ("9invalid_email@test.c",)),
    ],
)
def test_convert__to__into_tuple(context, mocker, settings, email, expected):
    send_email_mocked = mocker.patch("async_email.tasks.send_email_template")

    send_template_email_task(
        to=(email,),
        template_name="fake_category",
        context=context,
        from_email="fake_from@example.com",
    )
    send_email_mocked.assert_called_once_with(
        context=context,
        template_name="fake_category",
        from_email="fake_from@example.com",
        to=expected,
    )


@pytest.mark.integration_test
def test_dynamic_task_creation(celery_worker, celery_app, settings):
    """
    Tasks are created dynamically based on the settings.ASYNC_EMAIL_TEMPLATES
    """
    from celery.task.control import inspect

    inspect = inspect()
    expected = [
        f"async_email.tasks.{template_name}"
        for template_name in settings.ASYNC_EMAIL_TEMPLATES.keys()
    ]
    assert expected in inspect.registered_tasks().values()
