import inspect
from typing import Tuple

import pytest

from async_email.email.template import Email


def test_if_email_class__is_an_abstract():
    assert inspect.isabstract(Email)


def test_if_send_method_is_abstract():
    assert "_send" in Email.__abstractmethods__


def test_if_send_method_only_accept_tuple():
    """
    The param "to" of the method Email.send only accepts tuple?
    """

    class FakeEmail(Email):
        def _send(self, to: Tuple[str]):  # NOSONAR
            pass

    with pytest.raises(ValueError):
        FakeEmail().send(to="fake@example.com")  # noqa
