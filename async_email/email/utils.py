import re
from email.utils import parseaddr

from async_email.email.exceptions import EmailDomainNotFound, InvalidEmailAddress
from dns.resolver import NXDOMAIN, Answer, resolve


def resolve_dns_mx_record(fqdn: str) -> Answer:
    """
    Ensures the MX record exists on the fqdn to avoid send an email that will
    never reach the recipient.
    """
    try:
        return resolve(fqdn, "MX")
    except NXDOMAIN:
        raise EmailDomainNotFound(f"No MX record found for domain: {fqdn}")


def validate_email_address(email: str, validate_existence_of_mx_record=False):
    expression = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b")
    _, extracted_email = parseaddr(email)
    fqdn = extracted_email.rsplit("@", 1)[-1]

    if not expression.match(extracted_email):
        raise InvalidEmailAddress(f"The email address is invalid: {extracted_email}")

    if validate_existence_of_mx_record:
        resolve_dns_mx_record(fqdn)
