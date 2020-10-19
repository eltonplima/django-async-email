from django.conf import settings
from django.core.management.base import BaseCommand

from async_email import send_email_template


class Command(BaseCommand):
    help = "Send email asynchronously"

    def add_arguments(self, parser):
        # parser.add_argument("poll_ids", nargs="+", type=int)
        pass

    def handle(self, *args, **options):
        send_email_template(
            to=("me@eltonplima.dev",),
            template_name="welcome",
            context={"name": "Elton Lima", "project_name": settings.PROJECT_NAME},
        )
        self.stdout.write(self.style.SUCCESS("Successfully sent"))
