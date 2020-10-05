from appconf import AppConf  # noqa
from django.conf import settings  # noqa


class AsyncEmailAppConf(AppConf):
    CHECK_MX_RECORD_BEFORE_SEND_EMAIL = False
    TEMPLATES = {}
    TASKS = {}

    class Meta:
        prefix = "async_email"
