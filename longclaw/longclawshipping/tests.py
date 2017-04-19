from django.test import TestCase
from longclaw.tests.utils import LongclawTestCase, AddressFactory
from longclaw.longclawshipping.forms import AddressForm

class AddressTest(LongclawTestCase):
    def test_create_address(self):
        """
        Test creating an address object via the api
        """
        data = {
            'name': 'Bob Testerson',
            'line_1': 'Bobstreet',
            'city': 'Bobsville',
            'postcode': 'BOB22 2BO',
            'country': 'UK'
        }
        self.post_test(data, 'longclaw_address_list')


class AddressFormTest(TestCase):

    def setUp(self):
        self.address = AddressFactory()

    def test_address_form(self):
        form = AddressForm(instance=self.address)
        self.assertTrue(form.is_valid())
