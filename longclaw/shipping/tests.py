import uuid
import mock
from decimal import Decimal

from django.test import TestCase
from django.test.client import RequestFactory
from django.forms.models import model_to_dict
from longclaw.tests.utils import LongclawTestCase, AddressFactory, CountryFactory, ShippingRateFactory, BasketItemFactory, catch_signal
from longclaw.shipping.forms import AddressForm
from longclaw.shipping.utils import get_shipping_cost
from longclaw.shipping.templatetags import longclawshipping_tags
from longclaw.configuration.models import Configuration
from longclaw.basket.signals import basket_modified
from longclaw.basket.utils import basket_id

from .models import Address, ShippingRate, clear_basket_rates, clear_address_rates
from .signals import address_modified
from .serializers import AddressSerializer


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


class ShippingBasketTests(LongclawTestCase):
    def setUp(self):
        """Create a basket with things in it
        """
        request = RequestFactory().get('/')
        request.session = {}
        self.bid = bid = basket_id(request)
        self.item = BasketItemFactory(basket_id=bid)
        BasketItemFactory(basket_id=bid)
        
        self.address = address = AddressFactory()
        
        self.rate1 = ShippingRate.objects.create(
            name='98d17c43-7e20-42bd-b603-a4c83c829c5a',
            rate=99,
            carrier='8717ca67-4691-4dff-96ec-c43cccd15241',
            description='313037e1-644a-4570-808a-f9ba82ecfb34',
            basket_id=bid,
        )
        
        self.rate2 = ShippingRate.objects.create(
            name='8e721550-594c-482b-b512-54dc1744dff8',
            rate=97,
            carrier='4f4cca35-1a7a-47ec-ab38-a9918e0c04af',
            description='eacb446d-eb17-4ea7-82c1-ac2f62a53a7d',
            basket_id=bid,
            destination=address,
        )
        
        self.rate3 = ShippingRate.objects.create(
            name='72991859-dc0b-463e-821a-bf8b04aaed2c',
            rate=95,
            carrier='0aa3c318-b045-4a96-a456-69b4cc71d46a',
            description='78b03c47-b20f-4f91-8161-47340367fb34',
            destination=address,
        )
    
    def test_basket_rate(self):
        # this tests that we get a basket rate that is just tied to the basket and nothing else
        # (i.e. this basket qualifies for free shipping or something like that)
        result = get_shipping_cost(Configuration(), name='98d17c43-7e20-42bd-b603-a4c83c829c5a', basket_id=self.bid)
        self.assertEqual(result["rate"], 99)
        self.assertEqual(result["description"], '313037e1-644a-4570-808a-f9ba82ecfb34')
    
    def test_basket_address_rate(self):
        # this tests that we get a rate tied to a particular basket and a particular address
        result = get_shipping_cost(
            Configuration(),
            name='8e721550-594c-482b-b512-54dc1744dff8',
            basket_id=self.bid,
            destination=self.address,
        )
        self.assertEqual(result["rate"], 97)
        self.assertEqual(result["description"], 'eacb446d-eb17-4ea7-82c1-ac2f62a53a7d')
    
    def test_address_rate(self):
        # this tests that we get a rate tied to a particular address
        result = get_shipping_cost(
            Configuration(),
            name='72991859-dc0b-463e-821a-bf8b04aaed2c',
            destination=self.address,
        )
        self.assertEqual(result["rate"], 95)
        self.assertEqual(result["description"], '78b03c47-b20f-4f91-8161-47340367fb34')
    
    def test_clear_basket_rates_is_connected(self):
        result = basket_modified.disconnect(clear_basket_rates)
        self.assertTrue(result)
        basket_modified.connect(clear_basket_rates)
    
    def test_clear_basket_rates(self):
        self.assertTrue(ShippingRate.objects.filter(pk__in=[self.rate1.pk, self.rate2.pk, self.rate3.pk]).exists())
        clear_basket_rates(sender=ShippingRate, basket_id=self.bid)
        self.assertFalse(ShippingRate.objects.filter(pk__in=[self.rate1.pk, self.rate2.pk]).exists())
        self.assertTrue(ShippingRate.objects.filter(pk__in=[self.rate3.pk]).exists())


class AddressModifiedSignalTest(LongclawTestCase):
    """Round trip API tests
    """
    def setUp(self):
        self.country = CountryFactory()
        self.address = AddressFactory()
        self.address_data = {
            'name': 'JANE DOE',
            'line_1': '1600 Pennsylvania Ave NW',
            'city': 'DC',
            'postcode': '20500',
            'country': self.country.pk,
        }
        
        request = RequestFactory().get('/')
        request.session = {}
        self.bid = bid = basket_id(request)
        self.item = BasketItemFactory(basket_id=bid)
        BasketItemFactory(basket_id=bid)
        
        self.ratedAddress = address = AddressFactory()
        
        self.rate1 = ShippingRate.objects.create(
            name='98d17c43-7e20-42bd-b603-a4c83c829c5a',
            rate=99,
            carrier='8717ca67-4691-4dff-96ec-c43cccd15241',
            description='313037e1-644a-4570-808a-f9ba82ecfb34',
            basket_id=bid,
        )
        
        self.rate2 = ShippingRate.objects.create(
            name='8e721550-594c-482b-b512-54dc1744dff8',
            rate=97,
            carrier='4f4cca35-1a7a-47ec-ab38-a9918e0c04af',
            description='eacb446d-eb17-4ea7-82c1-ac2f62a53a7d',
            basket_id=bid,
            destination=address,
        )
        
        self.rate3 = ShippingRate.objects.create(
            name='72991859-dc0b-463e-821a-bf8b04aaed2c',
            rate=95,
            carrier='0aa3c318-b045-4a96-a456-69b4cc71d46a',
            description='78b03c47-b20f-4f91-8161-47340367fb34',
            destination=address,
        )
    
    def test_clear_address_rates_is_connected(self):
        result = address_modified.disconnect(clear_address_rates)
        self.assertTrue(result)
        address_modified.connect(clear_address_rates)
    
    def test_clear_address_rates(self):
        self.assertTrue(ShippingRate.objects.filter(pk__in=[self.rate1.pk, self.rate2.pk, self.rate3.pk]).exists())
        clear_address_rates(sender=ShippingRate, instance=self.ratedAddress)
        self.assertTrue(ShippingRate.objects.filter(pk__in=[self.rate1.pk]).exists())
        self.assertFalse(ShippingRate.objects.filter(pk__in=[self.rate2.pk, self.rate3.pk]).exists())

    def test_create_address_sends_signal(self):
        with catch_signal(address_modified) as handler:
            self.post_test(self.address_data, 'longclaw_address_list')
        
        handler.assert_called_once_with(
            instance=mock.ANY,
            sender=Address,
            signal=address_modified,
        )

    def test_put_address_sends_signal(self):
        serializer = AddressSerializer(self.address)
        data = {}
        data.update(serializer.data)
        data.update(self.address_data)
        
        self.assertNotEqual(self.address.postcode, '20500')
        
        with catch_signal(address_modified) as handler:
            response = self.put_test(data, 'longclaw_address_detail', urlkwargs={'pk': self.address.pk})
        
        self.assertEqual('20500', response.data['postcode'])
        
        handler.assert_called_once_with(
            instance=self.address,
            sender=Address,
            signal=address_modified,
        )
    
    def test_patch_address_sends_signal(self):
        self.assertNotEqual(self.address.postcode, '20500')
        
        with catch_signal(address_modified) as handler:
            response = self.patch_test(self.address_data, 'longclaw_address_detail', urlkwargs={'pk': self.address.pk})
        
        self.assertEqual('20500', response.data['postcode'])
        
        handler.assert_called_once_with(
            instance=self.address,
            sender=Address,
            signal=address_modified,
        )
    
    def test_delete_address_sends_signal(self):
        with catch_signal(address_modified) as handler:
            self.del_test('longclaw_address_detail', urlkwargs={'pk': self.address.pk})
        
        handler.assert_called_once_with(
            instance=mock.ANY,
            sender=Address,
            signal=address_modified,
        )


class AddressFormTest(TestCase):

    def setUp(self):
        self.address = AddressFactory()

    def test_address_form(self):
        form = AddressForm(data=model_to_dict(self.address))
        self.assertTrue(form.is_valid(), form.errors.as_json())


def simple_basket_id(request):
    return 'foo'


@mock.patch('longclaw.basket.utils.basket_id', side_effect=simple_basket_id)
class ShippingCostEndpointTest(LongclawTestCase):
    def setUp(self):
        self.country = CountryFactory()
        self.address = AddressFactory()
        
        request = RequestFactory().get('/')
        request.session = {}
        
        self.basket_id = basket_id(request)
        BasketItemFactory(basket_id=self.basket_id)
        BasketItemFactory(basket_id=self.basket_id)
        
        self.rate1 = ShippingRate.objects.create(
            name='rate1',
            rate=99,
            carrier='rate1c',
            description='rate1d',
            basket_id=self.basket_id,
        )
        
        self.rate2 = ShippingRate.objects.create(
            name='rate2',
            rate=97,
            carrier='rate2c',
            description='rate2d',
            basket_id=self.basket_id,
            destination=self.address,
        )
        
        self.rate3 = ShippingRate.objects.create(
            name='rate3',
            rate=95,
            carrier='rate3c',
            description='rate3d',
            destination=self.address,
        )
        
        self.rate4 = ShippingRate.objects.create(
            name='rate4',
            rate=93,
            carrier='rate4c',
            description='rate4d',
        )
        self.rate4.countries.add(self.country)
    
    def test_get_rate1_cost(self, basket_id_func):
        params = dict(
            country_code=self.country.pk,
            shipping_rate_name='rate1',
        )
        response = self.get_test('longclaw_shipping_cost', params=params)
        self.assertEqual(response.data, {'description': 'rate1d', 'rate': Decimal('99.00'), 'carrier': 'rate1c'})
    
    def test_get_rate2_cost(self, basket_id_func):
        params = dict(
            destination=self.address.pk,
            shipping_rate_name='rate2',
        )
        response = self.get_test('longclaw_shipping_cost', params=params)
        self.assertEqual(response.data, {'description': 'rate2d', 'rate': Decimal('97.00'), 'carrier': 'rate2c'})
    
    def test_get_rate3_cost(self, basket_id_func):
        params = dict(
            destination=self.address.pk,
            shipping_rate_name='rate3',
        )
        response = self.get_test('longclaw_shipping_cost', params=params)
        self.assertEqual(response.data, {'description': 'rate3d', 'rate': Decimal('95.00'), 'carrier': 'rate3c'})
    
    def test_get_rate4_cost(self, basket_id_func):
        # 
        # destination
        # 
        params = dict(
            country_code=self.country.pk,
            shipping_rate_name='rate4',
        )
        response = self.get_test('longclaw_shipping_cost', params=params)
        self.assertEqual(response.data, {'description': 'rate4d', 'rate': Decimal('93.00'), 'carrier': 'rate4c'})
        
        
        
        
        
