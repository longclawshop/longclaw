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
    ]


    @property
    def first_image(self):
        return self.images.first()

class ProductVariant(ProductVariantBase):
    '''Basic product variant for testing
    '''
    product = ParentalKey(Product, related_name='variants')
    description = RichTextField()
