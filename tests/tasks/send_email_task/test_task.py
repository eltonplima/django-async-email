from datetime import datetime
from time import sleep

import pytest
from freezegun import freeze_time

from async_email.tasks import send_email_task


def test_custom_from_email(context, mocker):
    send_email_mocked = mocker.patch("async_email.tasks.send_email")

    send_email_task(
        to=("noreply@example.com",),
        email_category="fake_category",
        context=context,
        from_email="fake_from@example.com",
    )
    send_email_mocked.assert_called_once_with(
        context=context,
        email_category="fake_category",
        from_email="fake_from@example.com",
        to=("noreply@example.com",),
    )


@freeze_time("2020-09-09")
def test_return(context, mocker):
    mocker.patch("async_email.tasks.send_email")

    result = send_email_task(
        to=("noreply@example.com",),
        email_category="fake_category",
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
    send_email_mocked = mocker.patch("async_email.tasks.send_email")

    send_email_task(
        to=(email,),
        email_category="fake_category",
        context=context,
        from_email="fake_from@example.com",
    )
    send_email_mocked.assert_called_once_with(
        context=context,
        email_category="fake_category",
        from_email="fake_from@example.com",
        to=expected,
    )


def test_dynamic_task_creation(celery_worker, celery_app, mocker):
    """
    Tasks are created dynamically based on the settings.ASYNC_EMAIL_TEMPLATES
    """
    wait_success_limit = 100
    send_email_mocked = mocker.patch("async_email.tasks.send_email")
    kwargs = {
        "email_category": "fake_category_a",
        "context": {},
        "to": "me@eltonplima.dev",
        "from_email": "contact@eltonplima.dev",
    }
    result = celery_app.send_task("fake_category_a", kwargs=kwargs,)

    while result.status != "SUCCESS" and wait_success_limit > 0:
        sleep(0.001)
        if wait_success_limit == 1:
            pytest.fail(
                f"[TIMEOUT] Waiting for the task to execute with success.\nLast known status was {result.status}"
            )
        wait_success_limit -= 1

    send_email_mocked.assert_called_once_with(**kwargs)
