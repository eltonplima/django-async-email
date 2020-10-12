import logging
from abc import ABCMeta
from abc import abstractmethod
from dataclasses import dataclass
from logging import Logger
from typing import Dict
from typing import Tuple

from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template import loader

from async_email.conf import settings
from async_email.email.utils import validate_email_address

logger: Logger = logging.getLogger(__name__)


@dataclass()
class Email(metaclass=ABCMeta):
    from_email: str

    def __post_init__(self):
        validate_email_address(self.from_email)

    @abstractmethod
    def _send(self, to: Tuple[str, ...]):
        raise NotImplementedError  # pragma: no cover

    def send(self, to: Tuple[str, ...]):
        if not isinstance(to, tuple):
            raise ValueError(f"Expected a tuple instance but received: {type(to)}")

        for email in to:
            validate_email_address(
                email=email,
                validate_existence_of_mx_record=settings.ASYNC_EMAIL_CHECK_MX_RECORD_BEFORE_SEND_EMAIL,
            )

        self._send(to=to)


@dataclass
class TemplateBasedEmail(Email):
    """
    Abstract the build of an email based on templates.
    """

    context: Dict
    email_template_name: str
    subject_template_name: str
    html_email_template_name: str = ""
    email_message_class: EmailMessage = EmailMultiAlternatives

    @property
    def subject(self) -> str:
        subject = loader.render_to_string(self.subject_template_name, self.context)
        # Email subject *must not* contain newlines
        return " ".join(subject.splitlines())

    @property
    def body_txt(self) -> str:
        return loader.render_to_string(self.email_template_name, self.context)

    @property
    def body_html(self) -> str:
        if self.html_email_template_name:
            return loader.render_to_string(self.html_email_template_name, self.context)

    def _send(self, to: Tuple[str, ...]):
        email = self.email_message_class(
            subject=self.subject, body=self.body_txt, from_email=self.from_email, to=to
        )
        if self.body_html is not None:
            email.attach_alternative(self.body_html, "text/html")

        email.send()


def email_template_factory(
    template_name: str, from_email: str = None, context: Dict = None
) -> TemplateBasedEmail:
    """
    Factory to create an instance of TemplateBasedEmail

    :param template_name: The category of email that will be send
    :param from_email: The sender email, if not set will be used what is
      declared on customer_settings:DEFAULT_FROM_EMAIL
    :param context: All the necessary context to build the email content.
    :return:
    """
    context = context or {}
    if template_name not in settings.ASYNC_EMAIL_TEMPLATES:
        categories = ", ".join(settings.ASYNC_EMAIL_TEMPLATES.keys())
        raise ValueError(
            f'The email category "{template_name}" was not found.\n'
            f"Please choose one of the following categories: {categories}"
        )
    email_templates = settings.ASYNC_EMAIL_TEMPLATES.get(template_name)
    html_email_body_name = email_templates.get("body_html")
    email_body_name = email_templates.get("body_txt")
    email_subject_name = email_templates.get("subject")
    from_email = from_email or settings.DEFAULT_FROM_EMAIL

    logger.debug(context)
    logger.debug(from_email)
    logger.debug(email_subject_name)
    logger.debug(html_email_body_name)
    logger.debug(email_body_name)

    return TemplateBasedEmail(
        context=context,
        html_email_template_name=html_email_body_name,
        email_template_name=email_body_name,
        subject_template_name=email_subject_name,
        from_email=from_email,
    )
