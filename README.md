# django-async-email

[![Actions Status](https://github.com/eltonplima/django-async-email/workflows/tox/badge.svg)](https://github.com/eltonplima/django-async-email/actions)
[![Actions Status](https://github.com/eltonplima/django-async-email/workflows/flake8/badge.svg)](https://github.com/eltonplima/django-async-email/actions)

```python
INSTALLED_APPS = [
...
"async_email",
]
```

```python
EMAILS_TEMPLATES = {
    "password_reset": {
        "subject": "registration/password_set_subject.txt",
        "body_html": "registration/password_set_email.html",
        "body_txt": "registration/password_set_email.txt",
    }
}
```
