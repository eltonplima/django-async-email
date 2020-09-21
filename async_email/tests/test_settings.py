DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:",}}

INSTALLED_APPS = (
    "async_email",
    "appconf",
)

SECRET_KEY = "fake secret key"

MIDDLEWARE_CLASSES = ()

TASKS = {}

EMAILS_TEMPLATES = {
    "fake_category": {
        "subject": "registration/password_set_subject.txt",
        "body_html": "registration/password_set_email.html",
        "body_txt": "registration/password_set_email.txt",
    }
}

CHECK_MX_RECORD_BEFORE_SEND_EMAIL = False
