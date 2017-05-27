from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.sites.models import Site
try:
  from django.urls import reverse
except ImportError:
  from django.core.urlresolvers import reverse

from longclaw.tests.utils import LongclawTestCase, AddressFactory, BasketItemFactory, CountryFactory, OrderFactory
from longclaw.longclawcheckout.utils import create_order
from longclaw.longclawcheckout.forms import CheckoutForm
from longclaw.longclawcheckout.views import CheckoutView
from longclaw.longclawcheckout.templatetags import longclawcheckout_tags as tags
from longclaw.longclawbasket.utils import basket_id


class CheckoutApiTest(LongclawTestCase):

    def setUp(self):

        self.addresses = {
            'shipping_name': '',
            'shipping_address_line1': '',
            'shipping_address_city': '',
            'shipping_address_zip': '',
            'shipping_address_country': '',
            'billing_name': '',
            'billing_address_line1': '',
            'billing_address_city': '',
            'billing_address_zip': '',
            'billing_address_country': ''
        }
        self.email = "test@test.com"
        self.request = RequestFactory().get('/')
        self.request.session = {}
        self.basket_id = basket_id(self.request)

    def test_create_order(self):
        BasketItemFactory(basket_id=self.basket_id),
        BasketItemFactory(basket_id=self.basket_id)
        order = create_order(self.email, self.request, self.addresses)
        self.assertIsNotNone(order)
        self.assertEqual(self.email, order.email)
        self.assertEqual(order.items.count(), 2)

    def test_checkout(self):
        """
        Test api endpoint checkout/
        """
        BasketItemFactory(basket_id=self.basket_id)
        BasketItemFactory(basket_id=self.basket_id)
        data = {
            'address': self.addresses,
            'email': self.email
        }
        self.post_test(data, 'longclaw_checkout', format='json')

    def test_checkout_prepaid(self):
        """
        Test api endpoint checkout/prepaid/
        """
        BasketItemFactory(basket_id=self.basket_id)
        data = {
            'address': self.addresses,
            'email': self.email,
            'transaction_id': 'blahblah'
        }
        self.post_test(data, 'longclaw_checkout_prepaid', format='json')

    def test_create_token(self):
        """
        Test api endpoint checkout/token/
        """
        self.get_test('longclaw_checkout_token')


class CheckoutTest(TestCase):

    def test_checkout_form(self):
        '''
        Test we can create the form without a shipping option
        '''
        data = {
            'email': 'test@test.com',
            'different_billing_address': False
        }
        form = CheckoutForm(data=data)
        self.assertTrue(form.is_valid(), form.errors.as_json())

    def test_invalid_checkout_form(self):
        '''
        Test making an invalid form
        '''
        form = CheckoutForm({
            'email': ''
        })
        self.assertFalse(form.is_valid())

    def test_get_checkout(self):
        '''
        Test the checkout GET view
        '''
        request = RequestFactory().get(reverse('longclaw_checkout_view'))
        response = CheckoutView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_post_checkout(self):
        '''
        Test correctly posting to the checkout view
        '''
        country = CountryFactory()
        request = RequestFactory().post(
            reverse('longclaw_checkout_view'),
            {
                'shipping-name': 'bob',
                'shipping-line_1': 'blah blah',
                'shipping-postcode': 'ytxx 23x',
                'shipping-city': 'London',
                'shipping-country': country.pk,
                'email': 'test@test.com'
            }
        )
        request.session = {}
        bid = basket_id(request)
        BasketItemFactory(basket_id=bid)
        response = CheckoutView.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_post_checkout_billing(self):
        '''
        Test using an alternate shipping
        address in the checkout view
        '''
        country = CountryFactory()
        request = RequestFactory().post(
            reverse('longclaw_checkout_view'),
            {
                'shipping-name': 'bob',
                'shipping-line_1': 'blah blah',
                'shipping-postcode': 'ytxx 23x',
                'shipping-city': 'London',
                'shipping-country': country.pk,
                'billing-name': 'john',
                'billing-line_1': 'somewhere',
                'billing-postcode': 'lmewrewr',
                'billing-city': 'London',
                'billing-country': country.pk,
                'email': 'test@test.com',
                'different_billing_address': True
            }
        )
        request.session = {}
        bid = basket_id(request)
        BasketItemFactory(basket_id=bid)
        response = CheckoutView.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_post_checkout_invalid(self):
        '''
        Test posting an invalid form.
        This should return a 200 response - rerendering
        the form page with the errors
        '''
        request = RequestFactory().post(
            reverse('longclaw_checkout_view')
        )
        request.session = {}
        bid = basket_id(request)
        BasketItemFactory(basket_id=bid)
        response = CheckoutView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_checkout_success(self):
        '''
        Test the checkout success view
        '''
        address = AddressFactory()
        order = OrderFactory(shipping_address=address, billing_address=address)
        response = self.client.get(reverse('longclaw_checkout_success', kwargs={'pk': order.id}))
        self.assertEqual(response.status_code, 200)



class GatewayTests(TestCase):

    def test_token_tag(self):
        token = tags.gateway_token()
        self.assertIsInstance(token, str)

    def test_js_tag(self):
        js = tags.gateway_client_js()
        self.assertIsInstance(js, (tuple, list))