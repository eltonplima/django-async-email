# send_email(subject, text_content, html_content, from_email, to)
# send_email_template(template_name, context, from_email, to)
from async_email import send_email_template


def test(mocker):
    email_factory_mocked = mocker.patch("async_email.email.email_factory")
    context = {"name": "fake name"}
    from_email = "noreply@example.com"
    to = ("contact@example.com",)
    template_name = "fake_category_a"
    send_email_template(
        template_name=template_name, context=context, from_email=from_email, to=to,
    )
    email_factory_mocked.assert_called_once_with(
        template_name=template_name, context=context, from_email=from_email
    )
