import mock

from longclaw.tests.utils import LongclawTestCase, AddressFactory, CountryFactory, BasketItemFactory
from longclaw.shipping.models import Address, ShippingRate, ShippingRateProcessor

from .models import TrivialShippingRateProcessor


@mock.patch('longclaw.shipping.api.basket_id', return_value='foo')
class TrivialShippingRateProcessorAPITest(LongclawTestCase):
    def setUp(self):
        self.country = CountryFactory()
        self.country.iso = '11'
        self.country.save()
        
        self.address = AddressFactory()
        self.address.country = self.country
        self.address.save()
        
        self.processor = TrivialShippingRateProcessor()
        self.processor.save()
        self.processor.countries.add(self.country)
    
    def add_item_to_basket(self):
        BasketItemFactory(basket_id='foo')
    
    def assert_contains_turtle(self, response):
        self.assertContains(response, 'turtle')
    
    def assert_contains_rabbit(self, response):
        self.assertContains(response, 'rabbit')
    
    def assert_contains_cheetah(self, response):
        self.assertContains(response, 'cheetah')
    
    def assert_not_contains_turtle(self, response):
        self.assertNotContains(response, 'turtle')
    
    def assert_not_contains_rabbit(self, response):
        self.assertNotContains(response, 'rabbit')
    
    def assert_not_contains_cheetah(self, response):
        self.assertNotContains(response, 'cheetah')
    
    def test_zero_rates(self, m1):
        params = {
            'destination': self.address.pk,
        }
        
        response = self.get_test('longclaw_applicable_shipping_rate_list', params=params)
        
        self.assertEqual(len(response.data), 0)
        self.assert_not_contains_turtle(response)
        self.assert_not_contains_rabbit(response)
        self.assert_not_contains_cheetah(response)
    
    def test_one_rate(self, m1):
        self.add_item_to_basket()
        
        params = {
            'destination': self.address.pk,
        }
        
        response = self.get_test('longclaw_applicable_shipping_rate_list', params=params)
        
        self.assertEqual(len(response.data), 1, response.content)
        self.assert_contains_turtle(response)
        self.assert_not_contains_rabbit(response)
        self.assert_not_contains_cheetah(response)
        
        return response
    
    def test_one_rate_cost(self, m1):
        rate_list_response = self.test_one_rate()
        rate = rate_list_response.data[0]
        self.assertIn('name', rate)
        name = rate['name']
        
        params = dict(
            destination=self.address.pk,
            shipping_rate_name=name,
        )
        response = self.get_test('longclaw_shipping_cost', params=params)
        self.assert_contains_turtle(response)
        self.assertIn('rate', response.data)
        self.assertEqual(response.data['rate'], 2)
    
    def test_two_rates(self, m1):
        self.add_item_to_basket()
        self.add_item_to_basket()
        
        params = {
            'destination': self.address.pk,
        }
        
        response = self.get_test('longclaw_applicable_shipping_rate_list', params=params)
        
        self.assertEqual(len(response.data), 2, response.content)
        self.assert_contains_turtle(response)
        self.assert_contains_rabbit(response)
        self.assert_not_contains_cheetah(response)
    
    def test_three_rates(self, m1):
        self.add_item_to_basket()
        self.add_item_to_basket()
        self.add_item_to_basket()
        
        params = {
            'destination': self.address.pk,
        }
        
        response = self.get_test('longclaw_applicable_shipping_rate_list', params=params)
        
        self.assertEqual(len(response.data), 3, response.content)
        self.assert_contains_turtle(response)
        self.assert_contains_rabbit(response)
        self.assert_contains_cheetah(response)
