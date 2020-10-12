__all__ = [
    "send_email_template",
]

from typing import Dict
from typing import Tuple

from django.conf import settings

from async_email.email.template import email_template_factory


def send_email_template(
    to: Tuple[str], template_name: str, from_email: str = None, context: Dict = None,
):
    """
    Helper function to send an email to one or more recipients.

    :param to: One or more destination email
    :param template_name: The category of email that we want to send. You
      will find this categories on customer.settings:EMAIL_TEMPLATES
    :param from_email: The sender email, if not set will be used what is
      declared on customer_settings:DEFAULT_FROM_EMAIL
    :param context: All the necessary context to build the email content.
    """
    if isinstance(to, str):
        to = (to,)
    else:
        to = tuple(to)

    from_email = from_email or settings.DEFAULT_FROM_EMAIL

    email = email_template_factory(
        template_name=template_name, from_email=from_email, context=context
    )
    email.send(to=to)
