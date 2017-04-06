from django.test.client import RequestFactory
from longclaw.tests.utils import LongclawTestCase, BasketItemFactory
from longclaw.longclawbasket.utils import basket_id


class BasketTest(LongclawTestCase):

    def setUp(self):
        request = RequestFactory().get('/')
        request.session = {}
        bid = basket_id(request)
        BasketItemFactory(basket_id=bid)

    def test_get_basket(self):
        self.get_test('longclaw_basket_list')

    def test_basket_total_items(self):
        self.get_test('longclaw_basket_total_items')
