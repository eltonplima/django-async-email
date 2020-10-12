import inspect

from async_email.email.template import Email


def test_if_email_class__is_an_abstract():
    assert inspect.isabstract(Email)


def test_if_send_method_is_abstract():
    assert "_send" in Email.__abstractmethods__
