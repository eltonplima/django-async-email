import inspect
from typing import Tuple
from unittest.mock import call

import pytest

from async_email.email.template import Email


@pytest.fixture()
def email_concrete_class():
    class FakeEmail(Email):
        def _send(self, to: Tuple[str]):  # NOSONAR
            pass

    return FakeEmail


def test_if_email_class__is_an_abstract():
    assert inspect.isabstract(Email)


def test_if_send_method_is_abstract():
    assert "_send" in Email.__abstractmethods__


def test_if_send_method_only_accept_tuple(email_concrete_class):
    """
    The param "to" of the method Email.send only accepts tuple?
    """
    with pytest.raises(ValueError):
        email_concrete_class().send(to="fake@example.com")  # noqa


def test_if_is_calling__validate_email_address__for_each_email(
    mocker, email_concrete_class, settings
):
    """
    When we call send with more than one destination email we validate
    each one of then?
    """
    validate_email_address_mocked = mocker.patch(
        "async_email.email.template.validate_email_address"
    )

    emails = ("contact@example.com", "noreply@example.com")

    email_template = email_concrete_class()
    email_template.send(to=emails)

    calls = [
        call(
            email="contact@example.com",
            validate_existence_of_mx_record=settings.ASYNC_EMAIL_CHECK_MX_RECORD_BEFORE_SEND_EMAIL,
        ),
        call(
            email="noreply@example.com",
            validate_existence_of_mx_record=settings.ASYNC_EMAIL_CHECK_MX_RECORD_BEFORE_SEND_EMAIL,
        ),
    ]
    validate_email_address_mocked.assert_has_calls(calls)
