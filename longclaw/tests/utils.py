import factory
from django.core.urlresolvers import reverse
from django.apps import apps
from django.utils.text import slugify

from rest_framework.test import APITestCase
from rest_framework import status

from wagtail_factories import PageFactory

from longclaw.longclawproducts.models import Product
from longclaw.longclawbasket.models import BasketItem
from longclaw.settings import PRODUCT_VARIANT_MODEL

ProductVariant = apps.get_model(*PRODUCT_VARIANT_MODEL.split('.'))

class ProductFactory(PageFactory):
    ''' Create a random Product
    '''
    class Meta:
        model = Product

    title = factory.Faker('sentence', nb_words=1)
    description = factory.Faker('text')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
      kwargs['parent'] = None
      return super(ProductFactory, cls)._create(model_class, *args, **kwargs)

class ProductVariantFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ProductVariant

    product = factory.SubFactory(ProductFactory)
    description = factory.Faker('text')  
    price = factory.Faker('pyfloat', positive=True, left_digits=2, right_digits=2)
    ref = factory.Faker('pystr', min_chars=3, max_chars=10)
    stock = factory.Faker('pyint')


class BasketItemFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = BasketItem

    quantity = 1
    variant = factory.SubFactory(ProductVariantFactory)

class LongclawTestCase(APITestCase):

    def get_test(self, urlname, urlkwargs=None, **kwargs):
        ''' Submit a GET request and assert the response status code is 200

        Arguments:
            urlname (str): The url name to pass to the 'reverse' function
            urlkwargs (dict): The `kwargs` parameter to pass to the `reverse` function
        '''
        response = self.client.get(reverse(urlname, kwargs=urlkwargs), **kwargs)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        return response

    def post_test(self, data, urlname, urlkwargs=None, **kwargs):
        ''' Submit a POST request and assert the response status code is 201

        Arguments:
            data (dict): The data to pass to the post request
            urlname (str): The url name to pass to the 'reverse' function
            urlkwargs (dict): The `kwargs` parameter to pass to the `reverse` function
        '''
        response = self.client.post(reverse(urlname, kwargs=urlkwargs), data, **kwargs)
        self.assertIn(response.status_code,
                      (status.HTTP_201_CREATED, status.HTTP_200_OK))
        return response

    def patch_test(self, data, urlname, urlkwargs=None, **kwargs):
        ''' Submit a PATCH request and assert the response status code is 200
        '''
        response = self.client.patch(reverse(urlname, kwargs=urlkwargs), data, **kwargs)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        return response

    def put_test(self, data, urlname, urlkwargs=None, **kwargs):
        response = self.client.put(reverse(urlname, kwargs=urlkwargs), data, **kwargs)
        self.assertEquals(response.status_code, status.HTTP_202_ACCEPTED)
        return response