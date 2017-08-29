from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.wagtailcore.fields import RichTextField
from longclaw.longclawproducts.models import ProductVariantBase, Product

class ProductVariant(ProductVariantBase):

    # Set 'Product' as the parent of product variants.
    # You can support your own 'Product' (and 'ProductIndex') pages
    # by change the referenced model below to your own, or
    # do away with the 'Product' concept entirely - e.g. if you only
    # want to support 1 'variant' per 'product'.
    product = ParentalKey(Product, related_name='variants')

    # Enter your custom product variant fields here
    # e.g. colour, size, stock and so on.
    # Remember, ProductVariantBase provides 'price', 'ref', 'slug' fields
    # and the parental key to the Product model.
    description = RichTextField()
