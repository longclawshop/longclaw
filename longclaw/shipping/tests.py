from django.test import TestCase
from django.forms.models import model_to_dict
from longclaw.tests.utils import LongclawTestCase, AddressFactory, CountryFactory, ShippingRateFactory
from longclaw.shipping.forms import AddressForm
from longclaw.shipping.utils import get_shipping_cost
from longclaw.shipping.templatetags import longclawshipping_tags
from longclaw.configuration.models import Configuration

class ShippingTests(LongclawTestCase):
    def setUp(self):
        self.country = CountryFactory()
    def test_create_address(self):
        """
        Test creating an address object via the api
        """
        data = {
            'name': 'Bob Testerson',
            'line_1': 'Bobstreet',
            'city': 'Bobsville',
            'postcode': 'BOB22 2BO',
            'country': self.country.pk
        }
        self.post_test(data, 'longclaw_address_list')

    def test_shipping_cost(self):
        sr = ShippingRateFactory(countries=[self.country])
        result = get_shipping_cost(Configuration(), self.country.pk, sr.name)
        self.assertEqual(result["rate"], sr.rate)

    def test_multiple_shipping_cost(self):
        sr = ShippingRateFactory(countries=[self.country])
        sr2 = ShippingRateFactory(countries=[self.country])
        result = get_shipping_cost(Configuration(), self.country.pk, sr.name)
        self.assertEqual(result["rate"], sr.rate)

    def test_default_shipping_cost(self):
        ls = Configuration(default_shipping_enabled=True)
        result = get_shipping_cost(ls)
        self.assertEqual(ls.default_shipping_rate, result["rate"])


class AddressFormTest(TestCase):

    def setUp(self):
        self.address = AddressFactory()

    def test_address_form(self):
        form = AddressForm(data=model_to_dict(self.address))
        self.assertTrue(form.is_valid(), form.errors.as_json())

