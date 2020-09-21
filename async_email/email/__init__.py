from typing import Dict, Tuple

from async_email.email.template import email_factory


def send_email(
    to: Tuple[str],
    email_category: str,
    from_email: str = None,
    context: Dict = None,
):
    """
    Helper function to send an email to one or more recipients.

    :param to: One or more destination email
    :param email_category: The category of email that we want to send. You
      will find this categories on customer.settings:EMAIL_TEMPLATES
    :param from_email: The sender email, if not set will be used what is
      declared on customer_settings:DEFAULT_FROM_EMAIL
    :param context: All the necessary context to build the email content.
    """

    email = email_factory(
        email_category=email_category, from_email=from_email, context=context
    )
    email.send(to=to)
