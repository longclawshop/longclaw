import uuid
from django.utils.encoding import force_text
from django.test import TestCase
from django.test.client import RequestFactory
from wagtail.core.models import Site
try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy

from longclaw.tests.utils import (
    LongclawTestCase,
    AddressFactory,
    BasketItemFactory,
    CountryFactory,
    OrderFactory
)
from longclaw.shipping.models import ShippingRate
from longclaw.checkout.utils import create_order
from longclaw.checkout.forms import CheckoutForm
from longclaw.checkout.views import CheckoutView
from longclaw.checkout.templatetags import longclawcheckout_tags as tags
from longclaw.basket.utils import basket_id


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
        order = create_order(self.email, self.request, self.addresses, capture_payment=True)
        self.assertIsNotNone(order)
        self.assertIsNotNone(order.payment_date)
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


class CheckoutApiShippingTest(LongclawTestCase):
    def setUp(self):
        self.shipping_address = AddressFactory()
        self.billing_address = AddressFactory()
        self.email = "test@test.com"
        self.request = RequestFactory().get('/')
        self.request.session = {}
        self.request.site = Site.find_for_request(self.request)
        self.basket_id = basket_id(self.request)
        BasketItemFactory(basket_id=self.basket_id)

    def test_create_order_with_basket_shipping_option(self):
        amount = 11
        rate = ShippingRate.objects.create(
            name=force_text(uuid.uuid4()),
            rate=amount,
            carrier=force_text(uuid.uuid4()),
            description=force_text(uuid.uuid4()),
            basket_id=self.basket_id,
        )
        order = create_order(
            self.email,
            self.request,
            shipping_address=self.shipping_address,
            billing_address=self.billing_address,
            shipping_option=rate.name,
        )
        self.assertEqual(order.shipping_rate, amount)
    
    def test_create_order_with_address_shipping_option(self):
        amount = 12
        rate = ShippingRate.objects.create(
            name=force_text(uuid.uuid4()),
            rate=amount,
            carrier=force_text(uuid.uuid4()),
            description=force_text(uuid.uuid4()),
            destination=self.shipping_address,
        )
        order = create_order(
            self.email,
            self.request,
            shipping_address=self.shipping_address,
            billing_address=self.billing_address,
            shipping_option=rate.name,
        )
        self.assertEqual(order.shipping_rate, amount)
    
    def test_create_order_with_address_and_basket_shipping_option(self):
        amount = 13
        rate = ShippingRate.objects.create(
            name=force_text(uuid.uuid4()),
            rate=amount,
            carrier=force_text(uuid.uuid4()),
            description=force_text(uuid.uuid4()),
            destination=self.shipping_address,
            basket_id=self.basket_id,
        )
        order = create_order(
            self.email,
            self.request,
            shipping_address=self.shipping_address,
            billing_address=self.billing_address,
            shipping_option=rate.name,
        )
        self.assertEqual(order.shipping_rate, amount)


class CheckoutTest(TestCase):

    def test_checkout_form(self):
        """
        Test we can create the form without a shipping option
        """
        data = {
            'email': 'test@test.com',
            'different_billing_address': False
        }
        form = CheckoutForm(data=data)
        self.assertTrue(form.is_valid(), form.errors.as_json())

    def test_invalid_checkout_form(self):
        """
        Test making an invalid form
        """
        form = CheckoutForm({
            'email': ''
        })
        self.assertFalse(form.is_valid())

    def test_get_checkout(self):
        """
        Test the checkout GET view
        """
        request = RequestFactory().get(reverse_lazy('longclaw_checkout_view'))
        response = CheckoutView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_post_checkout(self):
        """
        Test correctly posting to the checkout view
        """
        country = CountryFactory()
        request = RequestFactory().post(
            reverse_lazy('longclaw_checkout_view'),
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
        """
        Test using an alternate shipping
        address in the checkout view
        """
        country = CountryFactory()
        request = RequestFactory().post(
            reverse_lazy('longclaw_checkout_view'),
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
        """
        Test posting an invalid form.
        This should return a 200 response - rerendering
        the form page with the errors
        """
        request = RequestFactory().post(
            reverse_lazy('longclaw_checkout_view')
        )
        request.session = {}
        bid = basket_id(request)
        BasketItemFactory(basket_id=bid)
        response = CheckoutView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_checkout_success(self):
        """
        Test the checkout success view
        """
        address = AddressFactory()
        order = OrderFactory(shipping_address=address, billing_address=address)
        response = self.client.get(reverse_lazy('longclaw_checkout_success', kwargs={'pk': order.id}))
        self.assertEqual(response.status_code, 200)



class GatewayTests(TestCase):

    def test_token_tag(self):
        token = tags.gateway_token()
        self.assertIsInstance(token, str)

    def test_js_tag(self):
        js = tags.gateway_client_js()
        self.assertIsInstance(js, (tuple, list))
