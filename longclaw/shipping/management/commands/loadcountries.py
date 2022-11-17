from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load world country data"

    def handle(self, *args, **options):
        call_command(
            "loaddata", "shipping_initial_latest.json", app_label="longclaw_shipping"
        )
        self.stdout.write(
            self.style.SUCCESS("Initial country data was loaded to the database")
        )
