from celery.app.task import Task


class TestAttributes:
    def test_retry_backoff(self, fake_task):
        assert hasattr(fake_task, "retry_backoff")
        fake_task()
        assert fake_task.retry_backoff

    def test_retry_kwargs(self, fake_task, mocker):
        assert not hasattr(fake_task, "retry_kwargs")
        Task.retry = mocker.Mock()

        fake_task.retry()
        Task.retry.assert_called_once_with(  # noqa
            **{
                "args": None,
                "countdown": None,
                "eta": None,
                "exc": None,
                "kwargs": None,
                "max_retries": None,
                "throw": True,
            }
        )

    def test_custom_retry_kwargs(self, fake_task, settings, mocker):
        retry_kwargs = {"max_retries": 66}
        settings.TASKS[fake_task.name] = retry_kwargs
        assert not hasattr(fake_task, "retry_kwargs")
        Task.retry = mocker.Mock()

        fake_task.retry()
        Task.retry.assert_called_once_with(  # noqa
            **{
                "args": None,
                "countdown": None,
                "eta": None,
                "exc": None,
                "kwargs": None,
                "max_retries": 66,
                "throw": True,
            }
        )

    def test_retry_backoff_max(self, fake_task):
        assert hasattr(fake_task, "retry_backoff_max")
        fake_task()
        assert fake_task.retry_backoff_max == 600

    def test_retry_jitter(self, fake_task):
        assert hasattr(fake_task, "retry_jitter")
        fake_task()
        assert fake_task.retry_jitter

    def test_time_limit(self, fake_task):
        assert fake_task.time_limit == 60
        fake_task()
        assert fake_task.time_limit == 60
