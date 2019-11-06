from unittest import mock
from contextlib import contextmanager

import factory
from django.urls import reverse_lazy

from rest_framework.test import APITestCase
from rest_framework import status

from wagtail_factories import PageFactory


from longclaw.basket.models import BasketItem
from longclaw.orders.models import Order
from longclaw.shipping.models import Address, Country, ShippingRate
from longclaw.utils import ProductVariant, maybe_get_product_model


@contextmanager
def catch_signal(signal):
    """
        Catch django signal and return the mocked call.
        https://medium.freecodecamp.org/how-to-testing-django-signals-like-a-pro-c7ed74279311
    """
    handler = mock.Mock()
    signal.connect(handler)
    yield handler
    signal.disconnect(handler)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

class CountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Country

    iso = factory.Faker('pystr', max_chars=2, min_chars=2)
    name_official = factory.Faker('text', max_nb_chars=128)
    name = factory.Faker('text', max_nb_chars=128)


class AddressFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Address

    name = factory.Faker('text', max_nb_chars=64)
    line_1 = factory.Faker('text', max_nb_chars=128)
    line_2 = factory.Faker('text', max_nb_chars=128)
    city = factory.Faker('text', max_nb_chars=64)
    postcode = factory.Faker('text', max_nb_chars=10)
    country = factory.SubFactory(CountryFactory)

class ShippingRateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShippingRate

    name = factory.Faker('text', max_nb_chars=32)
    rate = 1.0
    carrier = 'Royal Mail'
    description = 'Test'

    @factory.post_generation
    def countries(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of countries were passed in, use them
            for country in extracted:
                self.countries.add(country)

class ProductFactory(PageFactory):
    """ Create a random Product
    """

    class Meta:
        model = maybe_get_product_model()

    title = factory.Faker('sentence', nb_words=1)
    description = factory.Faker('text')

class ProductVariantFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ProductVariant

    product = factory.SubFactory(ProductFactory)
    description = factory.Faker('text')
    base_price = factory.Faker('pyfloat', positive=True, left_digits=2, right_digits=2)
    ref = factory.Faker('pystr', min_chars=3, max_chars=10)
    stock = factory.Faker('pyint')


class BasketItemFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = BasketItem

    quantity = 1
    variant = factory.SubFactory(ProductVariantFactory)

class LongclawTestCase(APITestCase):

    def get_test(self, urlname, urlkwargs=None, params=None, success_expected=True, **kwargs):
        """ Submit a GET request and assert the response status code is 200

        Arguments:
            urlname (str): The url name to pass to the 'reverse_lazy' function
            urlkwargs (dict): The `kwargs` parameter to pass to the `reverse_lazy` function
        """
        params = params or {}
        response = self.client.get(reverse_lazy(urlname, kwargs=urlkwargs), params, **kwargs)
        if success_expected:
            self.assertTrue(status.is_success(response.status_code), response.content)
        return response

    def post_test(self, data, urlname, urlkwargs=None, success_expected=True, **kwargs):
        """ Submit a POST request and assert the response status code is 201

        Arguments:
            data (dict): The data to pass to the post request
            urlname (str): The url name to pass to the 'reverse_lazy' function
            urlkwargs (dict): The `kwargs` parameter to pass to the `reverse_lazy` function
        """
        response = self.client.post(reverse_lazy(urlname, kwargs=urlkwargs), data, **kwargs)
        if success_expected:
            self.assertTrue(status.is_success(response.status_code), response.content)
        return response

    def patch_test(self, data, urlname, urlkwargs=None, success_expected=True, **kwargs):
        """ Submit a PATCH request and assert the response status code is 200
        """
        response = self.client.patch(reverse_lazy(urlname, kwargs=urlkwargs), data, **kwargs)
        if success_expected:
            self.assertTrue(status.is_success(response.status_code), response.content)
        return response

    def put_test(self, data, urlname, urlkwargs=None, success_expected=True, **kwargs):
        response = self.client.put(reverse_lazy(urlname, kwargs=urlkwargs), data, **kwargs)
        if success_expected:
            self.assertTrue(status.is_success(response.status_code), response.content)
        return response

    def del_test(self, urlname, urlkwargs=None, success_expected=True, **kwargs):
        response = self.client.delete(reverse_lazy(urlname, kwargs=urlkwargs), **kwargs)
        if success_expected:
            self.assertTrue(status.is_success(response.status_code), response.content)
        return response
