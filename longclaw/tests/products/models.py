from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from longclaw.longclawproducts.models import ProductVariantBase, ProductBase

class ProductIndex(Page):
    '''Index page for all products
    '''
    subpage_types = ('products.Product', 'products.ProductIndex')


class Product(ProductBase):
    parent_page_types = ['products.ProductIndex']
    description = RichTextField()
    content_panels = ProductBase.content_panels + [
        FieldPanel('description'),
        InlinePanel('variants')
    ]


class ProductVariant(ProductVariantBase):
    '''Basic product variant for testing
    '''
    product = ParentalKey('products.Product', related_name='variants')
    description = RichTextField()

    @ProductVariantBase.price.getter
    def price(self):
        """Make the price dynamic to check that longclaw works with ``get_price``
        """
        return self.base_price * 10
