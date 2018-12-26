from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Load world country data'

    def handle(self, *args, **options):
        call_command('loaddata', 'shipping_initial.json', app_label='shipping')
        self.stdout.write(self.style.SUCCESS('Initial country data was loaded to the database'))
