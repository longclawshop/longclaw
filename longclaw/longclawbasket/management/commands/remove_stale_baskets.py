import datetime
from django.core.management import BaseCommand
from longclaw.longclawbasket.models import BasketItem

class Command(BaseCommand):
    """Remove old BasketItems.
    This command can be used in conjunction with e.g. a cron job
    to stop your database being polluted with abandoned basket items.
    """
    help = "Remove baskets older than the given number of days"

    def add_arguments(self, parser):
        parser.add_argument('older_than_days', type=int)

    # A command must define handle()
    def handle(self, *args, **options):
        days_old = options['older_than_days']
        today = datetime.date.today()
        date = today - datetime.timedelta(days=days_old)

        qrs = BasketItem.objects.filter(date_added__lt=date)
        count = qrs.count()
        qrs.delete()

        self.stdout.write(self.style.SUCCESS("Deleted {} basket items".format(count)))
