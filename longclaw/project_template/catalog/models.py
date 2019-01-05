from django.db import models
from django_extensions.db.fields import AutoSlugField
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from longclaw.products.models import ProductVariantBase, ProductBase

class ProductIndex(Page):
    """Index page for all products
    """
    subpage_types = ('catalog.Product', 'catalog.ProductIndex')


class Product(ProductBase):
    parent_page_types = ['catalog.ProductIndex']
    description = RichTextField()
    content_panels = ProductBase.content_panels + [
        FieldPanel('description'),
        InlinePanel('images', label='Images'),
        InlinePanel('variants', label='Product variants'),

    ]

    @property
    def first_image(self):
        return self.images.first()


class ProductVariant(ProductVariantBase):
    """Represents a 'variant' of a product
    """
    # You *could* do away with the 'Product' concept entirely - e.g. if you only
    # want to support 1 'variant' per 'product'.
    product = ParentalKey(Product, related_name='variants')

    slug = AutoSlugField(
        separator='',
        populate_from=('product', 'ref'),
        )

    # Enter your custom product variant fields here
    # e.g. colour, size, stock and so on.
    # Remember, ProductVariantBase provides 'price', 'ref' and 'stock' fields
    description = RichTextField()


class ProductImage(Orderable):
    """Example of adding images related to a product model
    """
    product = ParentalKey(Product, related_name='images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    caption = models.CharField(blank=True, max_length=255)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption')
    ]
