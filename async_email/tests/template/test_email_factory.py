import pytest
from async_email.email.template import email_factory


def test_with_invalid_category(template_based_email_instance, context):
    with pytest.raises(ValueError):
        email_factory(
            email_category="non_existent_category",
            from_email="fake@example.com",
            context=context,
        )


def test_with_valid_category(template_based_email_instance, context, settings, mocker):
    mocked_email = mocker.Mock()
    mocked = mocker.patch(
        "async_email.email.template.TemplateBasedEmail", return_value=mocked_email
    )

    email = email_factory(
        email_category="fake_category", from_email="fake@example.com", context=context,
    )

    assert email == mocked_email
    mocked.assert_called_once_with(
        context=context,
        email_template_name="registration/password_set_email.txt",
        from_email="fake@example.com",
        html_email_template_name="registration/password_set_email.html",
        subject_template_name="registration/password_set_subject.txt",
    )
