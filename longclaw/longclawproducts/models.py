from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django_extensions.db.fields import AutoSlugField

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

# Abstract base classes a user can use to implement their own product system

@python_2_unicode_compatible
class ProductBase(Page):
    '''Base classes for ``Product`` implementations. All this provides are
    a few helper methods for ``ProductVariant``'s. It assumes that ``ProductVariant``'s
    have a ``related_name`` of ``variants``
    '''

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    @property
    def price_range(self):
        ''' Calculate the price range of the products variants
        '''
        ordered = self.variants.order_by('price')
        if ordered:
            return ordered.first().price, ordered.last().price
        else:
            return None, None

    @property
    def in_stock(self):
        ''' Returns True if any of the product variants are in stock
        '''
        return any(self.variants.filter(stock__gt=0))


@python_2_unicode_compatible
class ProductVariantBase(models.Model):
    """
    Base model for creating product variants
    """
    price = models.DecimalField(max_digits=12, decimal_places=2)
    ref = models.CharField(max_length=32)
    stock = models.IntegerField(default=0)
    slug = AutoSlugField(
        separator='',
        populate_from=('product', 'ref'),
        )
    class Meta:
        abstract = True

    def __str__(self):
        return "{} - {}".format(self.product.title, self.ref)

    def get_product_title(self):
        return self.product.title

# Concrete models. These models do not need to be used in a user implementation.

class ProductIndex(Page):
    '''Index page for all products
    '''
    subpage_types = ('longclawproducts.Product', 'longclawproducts.ProductIndex')


class Product(ProductBase):
    parent_page_types = ['longclawproducts.ProductIndex']

    tags = ClusterTaggableManager(through='longclawproducts.ProductTag', blank=True)
    description = RichTextField()

    search_fields = Page.search_fields + [
        index.RelatedFields('tags', [
            index.SearchField('name', partial_match=True, boost=10),
        ]),
    ]

    content_panels = ProductBase.content_panels + [
        FieldPanel('description'),
        FieldPanel('tags'),
        InlinePanel('images', label='Product images'),
    ]


    @property
    def first_image(self):
        return self.images.first()


class ProductTag(TaggedItemBase):
    '''Tags for products
    '''
    content_object = ParentalKey('longclawproducts.Product', related_name='tagged_items')

class ProductImage(Orderable):
    """Images related to ``Product``
    """
    product = ParentalKey(Product, related_name='images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    caption = models.CharField(blank=True, max_length=255)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption')
    ]
