from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from longclaw.products.models import ProductVariantBase, ProductBase

class ProductIndex(Page):
    """Index page for all products
    """
    subpage_types = ('Product', 'ProductIndex')


class Product(ProductBase):
    parent_page_types = [ProductIndex]
    description = RichTextField()
    content_panels = ProductBase.content_panels + [
        FieldPanel('description'),
        InlinePanel('variants')
    ]


class ProductVariant(ProductVariantBase):
    """Basic product variant for testing
    """
    product = ParentalKey(Product, related_name='variants')
    description = RichTextField()

    @ProductVariantBase.price.getter
    def price(self):
        """Make the price dynamic to check that longclaw works with ``get_price``
        """
        return self.base_price * 10
