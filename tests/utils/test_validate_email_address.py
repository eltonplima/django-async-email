from unittest.mock import call

import pytest

from async_email.email.exceptions import InvalidEmailAddress
from async_email.email.utils import validate_email_address


@pytest.mark.parametrize(
    "email",
    [
        "",
        "invalid",
        "invalid-with-hyphen",
        "@invalid_email",
        "invalid_email@",
        "invalid_email@t.t",
        "invalid_email@test.c",
        "9invalid_email@test.c",
    ],
)
def test_with_invalid_email(email):
    with pytest.raises(InvalidEmailAddress):
        validate_email_address(email)


@pytest.mark.parametrize(
    "email",
    [
        "valid@example.com",
        "valid-email@example.com",
        "valid_email@example.com",
        "valid@example.com",
        "Foo Bar <valid@example.com>",
    ],
)
def test_with_valid_email(email):
    try:
        validate_email_address(email)
    except Exception:
        pytest.fail()


@pytest.mark.parametrize(
    "validate_existence_of_mx_record, calls",
    [
        (True, [call("example.com")]),
        (False, []),
    ],
)
def test_if__resolve_dns_mx_record__is_called(
    mocker, validate_existence_of_mx_record, calls
):
    """
    When the parameter validate_existence_of_mx_record is set the function
    resolve_dns_mx_record must be called.
    """
    mocked_resolve_dns_mx_record = mocker.patch(
        "async_email.email.utils.resolve_dns_mx_record"
    )

    validate_email_address(
        "contact@example.com",
        validate_existence_of_mx_record=validate_existence_of_mx_record,
    )

    mocked_resolve_dns_mx_record.assert_has_calls(calls)


def test_default_value_of_param_validate_existence_of_mx_record(
    mocker,
):
    mocked_resolve_dns_mx_record = mocker.patch(
        "async_email.email.utils.resolve_dns_mx_record"
    )

    validate_email_address("contact@example.com")

    mocked_resolve_dns_mx_record.assert_not_called()
