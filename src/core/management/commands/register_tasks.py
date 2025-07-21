from django.core.management.base import BaseCommand
from core.tasks import register_periodic_tasks


class Command(BaseCommand):
    help = "Register periodic tasks"

    def handle(self, *args, **options):
        self.stdout.write("Registering periodic tasks...")
        register_periodic_tasks()
        self.stdout.write(self.style.SUCCESS("Successfully registered periodic tasks"))