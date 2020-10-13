from email.utils import parseaddr

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from dns.resolver import NXDOMAIN
from dns.resolver import Answer
from dns.resolver import query

from async_email.email.exceptions import EmailDomainNotFound
from async_email.email.exceptions import InvalidEmailAddress


def resolve_dns_mx_record(fqdn: str) -> Answer:
    """
    Ensures the MX record exists on the fqdn to avoid send an email that will
    never reach the recipient.
    """
    try:
        return query(fqdn, "MX")
    except NXDOMAIN:
        raise EmailDomainNotFound(f"No MX record found for domain: {fqdn}")


def validate_email_address(email: str, validate_existence_of_mx_record=False):
    _, extracted_email = parseaddr(email)

    try:
        validate_email(extracted_email)
    except ValidationError:
        raise InvalidEmailAddress(f"The email address is invalid: {extracted_email}")

    if validate_existence_of_mx_record:
        fqdn = extracted_email.rsplit("@", 1)[-1]
        resolve_dns_mx_record(fqdn)
