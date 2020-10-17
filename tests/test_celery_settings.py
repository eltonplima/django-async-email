from kombu import Queue


def test_if_celery_task_queues__is_loaded_dynamically(settings):
    expected = (
        Queue("async_email.tasks.fake_category_a"),
        Queue("async_email.tasks.fake_category_b"),
    )
    assert settings.CELERY_TASK_QUEUES == expected
