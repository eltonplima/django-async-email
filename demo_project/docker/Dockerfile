FROM python:3.9

ENV PATH=/app/.venv/bin:${PATH}
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY pyproject.toml .
COPY poetry.lock .
RUN pip install -U pip setuptools poetry && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-dev
COPY . .
RUN python manage.py migrate

ENTRYPOINT ["python", "/app/manage.py"]
CMD ["runserver", "0:8000"]
