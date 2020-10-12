from async_email.email.template import Email
from async_email.email.template import TemplateBasedEmail


def test_superclass():
    assert issubclass(
        TemplateBasedEmail, Email
    ), "The class TemplateBasedEmail is not a subclass of Email"


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
