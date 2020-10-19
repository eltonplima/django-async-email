from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from async_email import send_email_template
from demo_project import settings


@receiver(post_save, sender=User)
def notify_user(instance: User, *args, **kwargs):
    result = send_email_template(
        to=(instance.email,),
        template_name="welcome",
        context={"name": instance.first_name, "project_name": settings.PROJECT_NAME},
    )
    print(args)
    print("=" * 80)
    print(kwargs)
    print("=" * 80)
    print(type(result))
    print(result)
