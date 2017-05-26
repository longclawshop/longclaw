from django.test import TestCase
from django.contrib.auth.models import User

from longclaw.tests.utils import LongclawTestCase, OrderFactory

class OrderApiTests(LongclawTestCase):

    def setUp(self):
        self.order = OrderFactory()

    def test_fulfill_order(self):
        self.post_test({}, 'longclaw_fulfill_order', urlkwargs={'pk': self.order.id})
