from async_email.email import send_email


def test_if_email_factory_is_called(mocker, context):
    email_mock = mocker.Mock()
    email_factory_patched = mocker.patch(
        "async_email.email.email_factory", return_value=email_mock
    )

    send_email(
        to=("fake@example.com",),
        email_category="reset",
        from_email="noreply@example.com",
        context=context,
    )

    email_factory_patched.assert_called_once_with(
        email_category="reset", from_email="noreply@example.com", context=context,
    )
    email_mock.send.assert_called_once_with(to=("fake@example.com",))


def test_default_from_email(context, mocker, settings):
    email_factory_mocked = mocker.patch("async_email.email.email_factory")
    settings.DEFAULT_FROM_EMAIL = "fake_from@example.com"

    send_email(
        to=("noreply@example.com",), email_category="fake_category", context=context
    )
    email_factory_mocked.assert_called_once_with(
        context=context,
        email_category="fake_category",
        from_email="fake_from@example.com",
    )


def test_if_email_string_on__to__parameter_is_converted_to_tuple(context, mocker):
    fake_email_class = mocker.Mock()
    mocker.patch("async_email.email.email_factory", return_value=fake_email_class)

    send_email(
        to="noreply@example.com", email_category="fake_category", context=context
    )
    fake_email_class.send.assert_called_once_with(to=("noreply@example.com",))
