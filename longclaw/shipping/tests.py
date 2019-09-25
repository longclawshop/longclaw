import uuid
import mock
from decimal import Decimal

from django.utils.encoding import force_text
from django.test import TestCase
from django.test.client import RequestFactory
from django.forms.models import model_to_dict
from longclaw.tests.utils import LongclawTestCase, AddressFactory, CountryFactory, ShippingRateFactory, BasketItemFactory, catch_signal
from longclaw.shipping.api import get_shipping_cost_kwargs
from longclaw.shipping.forms import AddressForm
from longclaw.shipping.models import Address, Country
from longclaw.shipping.utils import get_shipping_cost, InvalidShippingCountry
from longclaw.shipping.templatetags import longclawshipping_tags
from longclaw.configuration.models import Configuration
from longclaw.basket.signals import basket_modified
from longclaw.basket.utils import basket_id
from rest_framework import status
from rest_framework.views import APIView
from  wagtail.core.models import Site

from .models import Address, ShippingRate, clear_basket_rates, clear_address_rates, ShippingRateProcessor
from .signals import address_modified
from .serializers import AddressSerializer, ShippingRateSerializer


def upgrade_to_api_request(request):
    # This extra step is required until https://github.com/encode/django-rest-framework/issues/6488
    # is resolved
    class DummyGenericViewsetLike(APIView):
        lookup_field = 'test'

        def reverse_action(view, *args, **kwargs):
            self.assertEqual(kwargs['kwargs']['test'], 1)
            return '/example/'

    response = DummyGenericViewsetLike.as_view()(request)
    view = response.renderer_context['view']
    view.request.site = Site.objects.first()
    return view.request


class ShippingTests(LongclawTestCase):
    def setUp(self):
        self.country = CountryFactory()
    
    def test_get_shipping_cost_kwargs_country_and_code(self):
        request = RequestFactory().get('/', { 'country_code': 'US' })
        api_request = upgrade_to_api_request(request)
        with self.assertRaises(InvalidShippingCountry):
            get_shipping_cost_kwargs(api_request, country=self.country.pk)
    
    def test_get_shipping_cost_kwargs_destination_does_not_exist(self):
        non_existant_pk = 2147483647
        self.assertFalse(Address.objects.filter(pk=non_existant_pk).exists())
        request = RequestFactory().get('/', { 'country_code': 'US', 'destination': str(non_existant_pk) })
        api_request = upgrade_to_api_request(request)
        with self.assertRaises(InvalidShippingCountry):
            get_shipping_cost_kwargs(api_request, country=self.country.pk)
    
    def test_get_shipping_cost_kwargs_no_country_or_code(self):
        request = RequestFactory().get('/')
        api_request = upgrade_to_api_request(request)
        with self.assertRaises(InvalidShippingCountry):
            get_shipping_cost_kwargs(api_request)
    
    def test_get_shipping_cost_kwargs_only_country_code(self):
        request = RequestFactory().get('/', { 'country_code': 'US' })
        api_request = upgrade_to_api_request(request)
        result = get_shipping_cost_kwargs(api_request)
        self.assertEqual(result['country_code'], 'US')
        self.assertEqual(result['destination'], None)
        self.assertEqual(result['basket_id'], basket_id(api_request))
        self.assertEqual(result['settings'], Configuration.for_site(api_request.site))
        self.assertEqual(result['name'], 'standard')
    
    def test_get_shipping_cost_kwargs_country_code_and_shipping_rate_name(self):
        request = RequestFactory().get('/', { 'country_code': 'US', 'shipping_rate_name': 'foo' })
        api_request = upgrade_to_api_request(request)
        result = get_shipping_cost_kwargs(api_request)
        self.assertEqual(result['country_code'], 'US')
        self.assertEqual(result['destination'], None)
        self.assertEqual(result['basket_id'], basket_id(api_request))
        self.assertEqual(result['settings'], Configuration.for_site(api_request.site))
        self.assertEqual(result['name'], 'foo')
    
    def test_get_shipping_cost_kwargs_only_country(self):
        request = RequestFactory().get('/')
        api_request = upgrade_to_api_request(request)
        result = get_shipping_cost_kwargs(api_request, country=self.country.pk)
        self.assertEqual(result['country_code'], self.country.pk)
        self.assertEqual(result['destination'], None)
        self.assertEqual(result['basket_id'], basket_id(api_request))
        self.assertEqual(result['settings'], Configuration.for_site(api_request.site))
        self.assertEqual(result['name'], 'standard')
    
    def test_get_shipping_cost_kwargs_only_country_known_iso(self):
        request = RequestFactory().get('/')
        api_request = upgrade_to_api_request(request)
        country = Country.objects.create(iso='ZZ', name_official='foo', name='foo')
        result = get_shipping_cost_kwargs(api_request, country=country.pk)
        self.assertEqual(result['country_code'], 'ZZ')
        self.assertEqual(result['destination'], None)
        self.assertEqual(result['basket_id'], basket_id(api_request))
        self.assertEqual(result['settings'], Configuration.for_site(api_request.site))
        self.assertEqual(result['name'], 'standard')
    
    def test_get_shipping_cost_kwargs_with_destination(self):
        destination = AddressFactory()
        request = RequestFactory().get('/', { 'destination': destination.pk })
        api_request = upgrade_to_api_request(request)
        result = get_shipping_cost_kwargs(api_request)
        self.assertEqual(result['country_code'], destination.country.pk)
        self.assertEqual(result['destination'], destination)
        self.assertEqual(result['basket_id'], basket_id(api_request))
        self.assertEqual(result['settings'], Configuration.for_site(api_request.site))
        self.assertEqual(result['name'], 'standard')
    
    def test_get_shipping_cost_kwargs_with_destination_and_country_code(self):
        destination = AddressFactory()
        request = RequestFactory().get('/', { 'destination': destination.pk, 'country_code': '11' })
        api_request = upgrade_to_api_request(request)
        result = get_shipping_cost_kwargs(api_request)
        self.assertNotEqual(str(destination.country.pk), '11')
        self.assertEqual(result['country_code'], '11')
        self.assertEqual(result['destination'], destination)
        self.assertEqual(result['basket_id'], basket_id(api_request))
        self.assertEqual(result['settings'], Configuration.for_site(api_request.site))
        self.assertEqual(result['name'], 'standard')
    
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


@mock.patch('longclaw.shipping.api.basket_id', return_value='foo')
class ShippingCostEndpointTest(LongclawTestCase):
    def setUp(self):
        self.country = CountryFactory()
        self.address = AddressFactory()
        
        request = RequestFactory().get('/')
        request.session = {}
        
        self.basket_id = 'foo'
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


class ShippingRateProcessorTest(LongclawTestCase):
    def setUp(self):
        pass
    
    def test_process_rates_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            ShippingRateProcessor().process_rates()
    
    def test_get_rates_cache(self):
        rates = [
            ShippingRate(pk=1),
            ShippingRate(pk=2),
            ShippingRate(pk=3),
        ]
        
        rates_alt = [
            ShippingRate(pk=4),
            ShippingRate(pk=5),
            ShippingRate(pk=6),
        ]
        
        self.assertNotEqual(rates, rates_alt)
        
        processor = ShippingRateProcessor()
        processor.process_rates = lambda **kwargs: rates
        processor.get_rates_cache_key = lambda **kwargs: force_text('foo')
        
        self.assertEqual(processor.get_rates(), rates)
        
        processor.process_rates = lambda **kwargs: rates_alt
        
        self.assertEqual(processor.get_rates(), rates)
        
        processor.get_rates_cache_key = lambda **kwargs: force_text('bar')
        
        self.assertEqual(processor.get_rates(), rates_alt)


class ShippingRateProcessorAPITest(LongclawTestCase):
    def setUp(self):
        self.country = CountryFactory()
        self.country.iso = '11'
        self.country.save()
        
        self.address = AddressFactory()
        self.address.country = self.country
        self.address.save()
        
        self.processor = ShippingRateProcessor()
        self.processor.save()
        self.processor.countries.add(self.country)
    
    def test_shipping_option_endpoint_without_destination(self):
        params = {
            'country_code': self.country.pk,
        }
        response = self.get_test('longclaw_applicable_shipping_rate_list', params=params, success_expected=False)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Destination address is required for rates to 11.")
    
    def test_shipping_option_endpoint_gets_processor_rates(self):
        params = {
            'destination': self.address.pk,
        }
        with mock.patch('longclaw.shipping.api.ShippingRateProcessor.get_rates') as mocked_get_rates:
            mocked_get_rates.return_value = []
            
            response = self.get_test('longclaw_applicable_shipping_rate_list', params=params)
            self.assertTrue(mocked_get_rates.called)
            self.assertEqual(mocked_get_rates.call_count, 1)
            
            processor = ShippingRateProcessor()
            processor.save()
            processor.countries.add(self.country)
            
            response = self.get_test('longclaw_applicable_shipping_rate_list', params=params)
            self.assertEqual(mocked_get_rates.call_count, 3)


class ShippingOptionEndpointTest(LongclawTestCase):
    def setUp(self):
        self.country = CountryFactory()
        self.country2 = CountryFactory()
        self.address = AddressFactory()
        self.address2 = AddressFactory()
        self.address2.country = self.country2
        self.address2.save()
        
        self.assertNotEqual(self.country.pk, self.country2.pk, 'Try again. Random got you!')
        
        
        request = RequestFactory().get('/')
        request.session = {}
        
        self.basket_id = 'bar'
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
        
        self.rate5 = ShippingRate.objects.create(
            name='rate5',
            rate=95,
            carrier='rate5c',
            description='rate5d',
            destination=self.address2,
        )

    @mock.patch('longclaw.shipping.api.basket_id', return_value='bar')
    def test_get_rate1rate4_option_urlkwargs(self, basket_id_func):
        """
            We expect rate1 because of the basket id.
            We expect rate4 because of the country.
        """
        expected_pks = [self.rate1.pk, self.rate4.pk]
        serializer = ShippingRateSerializer(ShippingRate.objects.filter(pk__in=expected_pks), many=True)
        response = self.get_test('longclaw_shipping_options', urlkwargs={'country': self.country.pk})
        self.assertEqual(len(response.data), len(expected_pks))
        self.assertEqual(response.data, serializer.data)
    
    @mock.patch('longclaw.shipping.api.basket_id', return_value='bar')
    def test_get_rate1rate4_option(self, basket_id_func):
        """
            We expect rate1 because of the basket id.
            We expect rate4 because of the country.
        """
        expected_pks = [self.rate1.pk, self.rate4.pk]
        serializer = ShippingRateSerializer(ShippingRate.objects.filter(pk__in=expected_pks), many=True)
        params = {
            'country_code': self.country.pk,
        }
        response = self.get_test('longclaw_applicable_shipping_rate_list', params=params)
        self.assertEqual(len(response.data), len(expected_pks))
        self.assertEqual(response.data, serializer.data)
    
    @mock.patch('longclaw.shipping.api.basket_id', return_value='bar')
    def test_get_rate1rate2rate3_option(self, basket_id_func):
        """
            We expect rate1 because of the basket id.
            We expect rate2 because of the destination address and basket id.
            We expect rate3 because of the destination address.
        """
        expected_pks = [self.rate1.pk, self.rate2.pk, self.rate3.pk]
        serializer = ShippingRateSerializer(ShippingRate.objects.filter(pk__in=expected_pks), many=True)
        params = {
            'destination': self.address.pk,
        }
        response = self.get_test('longclaw_applicable_shipping_rate_list', params=params)
        self.assertEqual(len(response.data), len(expected_pks))
        self.assertEqual(response.data, serializer.data)
    
    def test_get_rate5_option(self):
        """
            We expect rate5 because of the destination address.
        """
        expected_pks = [self.rate5.pk]
        serializer = ShippingRateSerializer(ShippingRate.objects.filter(pk__in=expected_pks), many=True)
        params = {
            'destination': self.address2.pk,
        }
        response = self.get_test('longclaw_applicable_shipping_rate_list', params=params)
        self.assertEqual(len(response.data), len(expected_pks))
        self.assertEqual(response.data, serializer.data)
    
    def test_get_rate4_option(self):
        """
            We expect rate4 because of the country.
        """
        expected_pks = [self.rate4.pk]
        serializer = ShippingRateSerializer(ShippingRate.objects.filter(pk__in=expected_pks), many=True)
        params = {
            'country_code': self.country.pk,
        }
        response = self.get_test('longclaw_applicable_shipping_rate_list', params=params)
        self.assertEqual(len(response.data), len(expected_pks))
        self.assertEqual(response.data, serializer.data)
    
    def test_get_rate4_option_urlkwargs(self):
        """
            We expect rate4 because of the country.
        """
        expected_pks = [self.rate4.pk]
        serializer = ShippingRateSerializer(ShippingRate.objects.filter(pk__in=expected_pks), many=True)
        response = self.get_test('longclaw_shipping_options', urlkwargs={'country': self.country.pk})
        self.assertEqual(len(response.data), len(expected_pks))
        self.assertEqual(response.data, serializer.data)
    
    @mock.patch('longclaw.shipping.api.basket_id', return_value='bar')
    def test_get_rate1_option(self, basket_id_func):
        """
            We expect rate1 because of the basket.
        """
        expected_pks = [self.rate1.pk]
        serializer = ShippingRateSerializer(ShippingRate.objects.filter(pk__in=expected_pks), many=True)
        params = {
            'country_code': self.country2.pk,
        }
        response = self.get_test('longclaw_applicable_shipping_rate_list', params=params)
        self.assertEqual(len(response.data), len(expected_pks))
        self.assertEqual(response.data, serializer.data)
    
    @mock.patch('longclaw.shipping.api.basket_id', return_value='bar')
    def test_get_rate6_option(self, basket_id_func):
        """
            We expect rate6 because of the basket id and address.
        """
        expected_pks = [self.rate1.pk]
        serializer = ShippingRateSerializer(ShippingRate.objects.filter(pk__in=expected_pks), many=True)
        params = {
            'country_code': self.country2.pk,
        }
        response = self.get_test('longclaw_applicable_shipping_rate_list', params=params)
        self.assertEqual(len(response.data), len(expected_pks))
        self.assertEqual(response.data, serializer.data)
    
        
        
        
        
        
