import inspect
from typing import Tuple
from typing import Type
from unittest.mock import call

import pytest

from async_email.email.template import Email


@pytest.fixture()
def email_concrete_class() -> Type[Email]:
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
        email_concrete_class(from_email="fake_from@example.com").send(
            to="fake@example.com"
        )  # noqa


def test_if_is_calling__validate_email_address__during_creation_of_the_instance(
    mocker, email_concrete_class
):
    validate_email_address_mocked = mocker.patch(
        "async_email.email.template.validate_email_address"
    )
    from_email = "contact@example.com"

    email_concrete_class(from_email=from_email)

    validate_email_address_mocked.assert_called_once_with(from_email)


class TestSend:
    def test_if_is_calling__validate_email_address__for_each_email_address_that_will_be_send(
        self, mocker, email_concrete_class, settings
    ):
        """
        When we call send with more than one destination email we validate
        each one of then?
        """
        validate_email_address_mocked = mocker.patch(
            "async_email.email.template.validate_email_address"
        )

        to_emails = ("contact@example.com", "noreply@example.com")

        email_template = email_concrete_class(from_email="fake_from@example.com")
        email_template.send(to=to_emails)

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

    @pytest.mark.parametrize(
        "check_before_send_email", [True, False],
    )
    def test__validate_email_address__with__validate_existence_of_mx_record__can_be_controlled_by_settings(
        self,
        mocker,
        context,
        mocked_template_loader,
        settings,
        check_before_send_email,
        email_concrete_class,
    ):
        """
        The flag validate_existence_of_mx_record of the function
        validate_email_address is controlled by the flag
        ASYNC_EMAIL_CHECK_MX_RECORD_BEFORE_SEND_EMAIL that lives on the django
        settings.
        """
        settings.ASYNC_EMAIL_CHECK_MX_RECORD_BEFORE_SEND_EMAIL = check_before_send_email
        validate_email_address_mocked = mocker.patch(
            "async_email.email.template.validate_email_address"
        )

        email = ("contact@example.com",)

        email_template = email_concrete_class(from_email="noreply@example.com")
        # Reset mock because this function is called on the class initialization too.
        validate_email_address_mocked.reset_mock()

        email_template.send(to=email)

        validate_email_address_mocked.assert_called_once_with(
            email=email[0], validate_existence_of_mx_record=check_before_send_email
        )
