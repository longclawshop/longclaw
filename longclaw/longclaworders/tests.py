import mock
from django.test import TestCase
from django.contrib.auth.models import User
try:
  from django.urls import reverse
except ImportError:
  from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from wagtail.tests.utils import WagtailTestUtils
from longclaw.tests.utils import LongclawTestCase, OrderFactory
from longclaw.longclaworders.wagtail_hooks import OrderModelAdmin

class OrderTests(LongclawTestCase):

    def setUp(self):
        self.order = OrderFactory(transaction_id="FAKE")
        admin = User.objects.create_superuser('admn', 'myemail@test.com', 'password')
        self.client.force_authenticate(user=admin)

    def test_fulfill_order(self):
        self.post_test({}, 'longclaw_fulfill_order', urlkwargs={'pk': self.order.id})
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, self.order.FULFILLED)

    def test_total(self):
        self.assertEqual(self.order.total, 0)

    def test_total_items(self):
        self.assertEqual(self.order.total_items, 0)

    def test_refund_order(self):
        self.post_test({}, 'longclaw_refund_order', urlkwargs={'pk': self.order.id})
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, self.order.REFUNDED)

    def test_cancel_order(self):
        self.order.cancel()
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, self.order.CANCELLED)


class TestOrderView(LongclawTestCase, WagtailTestUtils):

    def setUp(self):
        self.login()
        self.model_admin = OrderModelAdmin()

    def test_order_index_view(self):
        """
        Test the index view
        """
        name = self.model_admin.url_helper.get_action_url_name('index')
        response = self.client.get(reverse(name))
        self.assertEqual(response.status_code, 200)

    def test_order_detail_view(self):
        order = OrderFactory()
        name = self.model_admin.url_helper.get_action_url_name('detail')
        response = self.client.get(reverse(name, kwargs={'instance_pk': order.pk}))
        self.assertEqual(response.status_code, 200)
