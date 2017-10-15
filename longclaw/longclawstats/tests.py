from datetime import datetime, timedelta
from django.test import TestCase
from django.utils import timezone

from longclaw.longclawstats import stats
from longclaw.tests.utils import OrderFactory

class StatsTest(TestCase):

    def setUp(self):
        order = OrderFactory()
        order.payment_date = timezone.now()
        order.save()

    def test_current_month(self):
        start, end = stats.current_month()
        self.assertEqual(start.month, end.month)
        self.assertEqual(start.day, 1)
        self.assertIn(end.day, [28, 29, 30, 31])

    def test_sales_for_time_period(self):
        delta = timedelta(days=1)
        sales = stats.sales_for_time_period(datetime.now() - delta, datetime.now() + delta)
        self.assertEqual(sales.count(), 1)

    def test_daily_sales(self):
        delta = timedelta(days=10)
        groups = stats.daily_sales(datetime.now() - delta, datetime.now() + delta)
        # We only create 1 order.
        self.assertEqual(len(list(groups)), 1)
