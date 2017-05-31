from django.test import TestCase
from django.contrib.auth.models import User

from longclaw.tests.utils import LongclawTestCase, OrderFactory

class OrderTests(LongclawTestCase):

    def setUp(self):
        self.order = OrderFactory()

    def test_fulfill_order(self):
        self.post_test({}, 'longclaw_fulfill_order', urlkwargs={'pk': self.order.id})

    def test_total(self):
        self.assertEqual(self.order.total, 0)

    def test_total_items(self):
        self.assertEqual(self.order.total_items, 0)
