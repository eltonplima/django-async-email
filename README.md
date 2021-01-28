# django-async-email

[![Actions Status](https://github.com/eltonplima/django-async-email/workflows/tox/badge.svg)](https://github.com/eltonplima/django-async-email/actions)
[![Actions Status](https://github.com/eltonplima/django-async-email/workflows/flake8/badge.svg)](https://github.com/eltonplima/django-async-email/actions)

```shell
pip install django-async-email
```

```python
INSTALLED_APPS = [
...
"async_email",
]
```

```python
# Associate a category with your templates
ASYNC_EMAIL_TEMPLATES = {
    "payments_receipts": {
        "subject": "payments_receipts/subject.txt",
        "body_html": "payments_receipts/body.html",
        "body_txt": "payments_receipts/body.txt",
    },
    "welcome": {
        "subject": "welcome/subject.txt",
        "body_html": "welcome/body.html",
        "body_txt": "welcome/body.txt",
    },

}

# Custom settings per task
ASYNC_EMAIL_TASKS = {
    "async_email.tasks.welcome": {"max_retries": 30},
    "async_email.tasks.payments_receipts": {"max_retries": 5},
}

ASYNC_EMAIL_CHECK_MX_RECORD_BEFORE_SEND_EMAIL = False

ASYNC_EMAIL_TASKS_MAX_RETRIES = 20  # Global max retries
```
