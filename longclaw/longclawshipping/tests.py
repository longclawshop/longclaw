from django.test import TestCase
from django.forms.models import model_to_dict
from longclaw.tests.utils import LongclawTestCase, AddressFactory, CountryFactory
from longclaw.longclawshipping.forms import AddressForm

class AddressTest(LongclawTestCase):
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


class AddressFormTest(TestCase):

    def setUp(self):
        self.address = AddressFactory()

    def test_address_form(self):
        form = AddressForm(data=model_to_dict(self.address))
        self.assertTrue(form.is_valid(), form.errors.as_json())
