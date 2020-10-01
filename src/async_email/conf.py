from django.conf import settings  # noqa
from appconf import AppConf  # noqa


class AsyncEmailAppConf(AppConf):
    CHECK_MX_RECORD_BEFORE_SEND_EMAIL = False
    EMAILS_TEMPLATES = {}
    TASKS = {}

    class Meta:
        prefix = "async_email"
