import pytest

from async_email.exceptions import MissingRequiredConfiguration


def test_settings_without_default_from_email(context, settings):
    with pytest.raises(MissingRequiredConfiguration):
        settings.DEFAULT_FROM_EMAIL = None
        import async_email  # noqa
