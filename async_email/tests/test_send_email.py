from async_email.email import send_email


def test(mocker, context):
    email_mock = mocker.Mock()
    email_factory_patched = mocker.patch(
        "async_email.email.email_factory", return_value=email_mock
    )

    send_email(
        to="fake@example.com",  # noqa
        email_category="reset",
        from_email="noreply@example.com",
        context=context,
    )

    email_factory_patched.assert_called_once_with(
        email_category="reset", from_email="noreply@example.com", context=context,
    )
    email_mock.send.assert_called_once_with(to="fake@example.com")
