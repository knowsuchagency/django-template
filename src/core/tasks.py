# tasks.py
from django_q.models import Schedule


def hello_world():
    print("Hello, world!")
    return "Hello, world!"


Schedule.objects.get_or_create(
    func="core.tasks.hello_world",
    name="Hello world",
    schedule_type=Schedule.CRON,
    cron="*/1 * * * *",
)
