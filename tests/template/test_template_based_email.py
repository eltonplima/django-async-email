import pytest

from async_email.email.template import Email
from async_email.email.template import TemplateBasedEmail


class TestSubject:
    def test_if_template_render_is_called(
        self, template_based_email_instance, mocked_template_loader, context
    ):
        assert template_based_email_instance.subject == "fake"
        mocked_template_loader.render_to_string.assert_called_once_with(
            "registration/password_set_subject.txt", context
        )

    def test_remove_new_line(
        self, template_based_email_instance, mocked_template_loader, context
    ):
        mocked_template_loader.render_to_string.return_value = (
            "My subject with\nnew line"
        )
        assert template_based_email_instance.subject == "My subject with new line"


def test_if_body_txt_is_calling_the_template_render(
    template_based_email_instance, mocked_template_loader, context
):
    assert template_based_email_instance.body_txt == "fake"
    mocked_template_loader.render_to_string.assert_called_once_with(
        "registration/password_set_email.txt", context
    )


def test_if_body_html_is_calling_the_template_render(
    template_based_email_instance, mocked_template_loader, context
):
    assert template_based_email_instance.body_html == "fake"
    mocked_template_loader.render_to_string.assert_called_once_with(
        "registration/password_set_email.html", context
    )


class TestSend:
    def test_without_html_template(self, mocker, context, mocked_template_loader):
        """
        When the parameter html_email_template_name is not set we send the
        email without html version?
        """
        mocked_email_instance = mocker.Mock()
        stub = mocker.Mock(return_value=mocked_email_instance)
        email = ("fake@example.com",)

        template_email = TemplateBasedEmail(
            context=context,
            email_template_name="registration/password_set_email.txt",
            subject_template_name="registration/password_set_subject.txt",
            from_email="noreply@example.com",
            email_message_class=stub,
        )
        template_email.send(to=email)

        stub.assert_called_once_with(
            body="fake", from_email="noreply@example.com", subject="fake", to=email,
        )
        mocked_email_instance.attach_alternative.assert_not_called()

    def test_with_html_template(self, mocker, context, mocked_template_loader):
        """
        When the parameter html_email_template_name is set we send the html
        version of the email too?
        """
        mocked_email_instance = mocker.Mock()
        stub = mocker.Mock(return_value=mocked_email_instance)
        email = ("fake@example.com",)

        template_email = TemplateBasedEmail(
            context=context,
            html_email_template_name="registration/password_set_email.html",
            email_template_name="registration/password_set_email.txt",
            subject_template_name="registration/password_set_subject.txt",
            from_email="noreply@example.com",
            email_message_class=stub,
        )
        template_email.send(to=email)

        stub.assert_called_once_with(
            body="fake", from_email="noreply@example.com", subject="fake", to=email,
        )
        mocked_email_instance.attach_alternative.assert_called_once_with(
            "fake", "text/html"
        )

    def test_if_is_calling__validate_email_address(
        self, mocker, context, mocked_template_loader, settings
    ):
        """
        The method TemplateBasedEmail.send is calling the function
        validate_email_address?
        """
        validate_email_address_mocked = mocker.patch(
            "async_email.email.template.validate_email_address"
        )
        stub = mocker.Mock()

        email = ("contact@example.com",)

        email_template = TemplateBasedEmail(
            context=context,
            html_email_template_name="registration/password_set_email.html",
            email_template_name="registration/password_set_email.txt",
            subject_template_name="registration/password_set_subject.txt",
            from_email=email[0],
            email_message_class=stub,
        )
        # Reset mock because this function is called on the class initialization too.
        validate_email_address_mocked.reset_mock()

        email_template.send(to=email)

        validate_email_address_mocked.assert_called_once_with(
            email=email[0],
            validate_existence_of_mx_record=settings.ASYNC_EMAIL_CHECK_MX_RECORD_BEFORE_SEND_EMAIL,
        )

    @pytest.mark.parametrize(
        "check_before_send_email", [True, False],
    )
    def test__validate_email_address__with__validate_existence_of_mx_record__can_be_controlled_by_settings(
        self, mocker, context, mocked_template_loader, settings, check_before_send_email
    ):
        """
        The flag validate_existence_of_mx_record of the function
        validate_email_address is controlled by the flag
        ASYNC_EMAIL_CHECK_MX_RECORD_BEFORE_SEND_EMAIL that lives on the django
        settings.
        """
        print(f"check_before_send_email: {check_before_send_email}".center(80, "="))
        settings.ASYNC_EMAIL_CHECK_MX_RECORD_BEFORE_SEND_EMAIL = check_before_send_email
        validate_email_address_mocked = mocker.patch(
            "async_email.email.template.validate_email_address"
        )

        email = ("contact@example.com",)

        email_template = TemplateBasedEmail(
            context=context,
            html_email_template_name="registration/password_set_email.html",
            email_template_name="registration/password_set_email.txt",
            subject_template_name="registration/password_set_subject.txt",
            from_email="noreply@example.com",
            email_message_class=mocker.Mock(),
        )
        # Reset mock because this function is called on the class initialization too.
        validate_email_address_mocked.reset_mock()

        email_template.send(to=email)

        validate_email_address_mocked.assert_called_once_with(
            email=email[0], validate_existence_of_mx_record=check_before_send_email
        )


def test_if_is_calling__validate_email_address__during_creation_of_the_instance(
    context, mocker
):
    validate_email_address_mocked = mocker.patch(
        "async_email.email.template.validate_email_address"
    )
    email = "contact@example.com"

    TemplateBasedEmail(
        context=context,
        html_email_template_name="registration/password_set_email.html",
        email_template_name="registration/password_set_email.txt",
        subject_template_name="registration/password_set_subject.txt",
        from_email=email,
    )

    validate_email_address_mocked.assert_called_once_with(email)


def test_superclass():
    assert issubclass(
        TemplateBasedEmail, Email
    ), "The class TemplateBasedEmail is not a subclass of Email"
