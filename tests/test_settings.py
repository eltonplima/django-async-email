DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:",}}

INSTALLED_APPS = (
    "async_email",
    "appconf",
)

SECRET_KEY = "fake secret key"

MIDDLEWARE_CLASSES = ()

ASYNC_EMAIL_TASKS = {}

ASYNC_EMAIL_TEMPLATES = {
    "fake_category_a": {
        "subject": "registration/password_set_subject.txt",
        "body_html": "registration/password_set_email.html",
        "body_txt": "registration/password_set_email.txt",
    },
    "fake_category_b": {
        "subject": "registration/password_set_subject.txt",
        "body_html": "registration/password_set_email.html",
        "body_txt": "registration/password_set_email.txt",
    },
}

ASYNC_EMAIL_CHECK_MX_RECORD_BEFORE_SEND_EMAIL = False
