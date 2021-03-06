import pytest
from async_email.email.exceptions import EmailDomainNotFound
from async_email.email.utils import resolve_dns_mx_record
from dns.resolver import NXDOMAIN


def test_if_is_calling_dns(mocker):
    mocked_dns_query = mocker.patch("async_email.email.utils.resolve")
    fqdn = "example.com"
    resolve_dns_mx_record(fqdn)
    mocked_dns_query.assert_called_once_with(fqdn, "MX")


def test_with_domain_not_exist(mocker):
    mocker.patch("async_email.email.utils.resolve", side_effect=NXDOMAIN)
    fqdn = "example.com"
    with pytest.raises(EmailDomainNotFound):
        resolve_dns_mx_record(fqdn)
