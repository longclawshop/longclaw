from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.wagtailcore.fields import RichTextField
from longclaw.longclawproducts.models import ProductVariantBase, Product

class ProductVariant(ProductVariantBase):
    '''Basic product variant for testing
    '''
    product = ParentalKey(Product, related_name='variants')
    description = RichTextField()
