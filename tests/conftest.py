import pytest
from django.template import loader

from async_email.email.template import TemplateBasedEmail
from async_email.task import BaseTask


@pytest.fixture(scope="function")
def fake_task(celery_app):
    @celery_app.task(base=BaseTask)
    def _fake_task():  # noqa
        pass

    return _fake_task


@pytest.fixture()
def context():
    return {
        "foo": "bar",
        "user_id": 666,
    }


@pytest.fixture()
def template_based_email_instance(context):
    return TemplateBasedEmail(
        context=context,
        html_email_template_name="registration/password_set_email.html",
        email_template_name="registration/password_set_email.txt",
        subject_template_name="registration/password_set_subject.txt",
        from_email="noreply@example.com",
    )


@pytest.fixture()
def mocked_template_loader(mocker):
    mocker.patch.object(loader, "render_to_string", return_value="fake")
    return loader


@pytest.fixture(scope="session")
def celery_config():
    return {"broker_url": "amqp://", "result_backend": "rpc"}
