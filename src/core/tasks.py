# tasks.py
from django_q.models import Schedule
from django.db.utils import OperationalError
from loguru import logger


def hello_world():
    print("Hello, world!")
    return "Hello, world!"


try:
    Schedule.objects.get_or_create(
        func="core.tasks.hello_world",
        name="Hello world",
        schedule_type=Schedule.CRON,
        cron="*/1 * * * *",
    )
except OperationalError:
    logger.warning("Database or migrations not ready, skipping task registration")
