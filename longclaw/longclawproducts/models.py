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

class ProductIndex(Page):
    subpage_types = ('longclawproducts.Product', 'longclawproducts.ProductIndex')

class ProductTag(TaggedItemBase):
    content_object = ParentalKey('Product', related_name='tagged_items')

class Product(Page):
    parent_page_types = ['longclawproducts.ProductIndex']
    description = RichTextField()
    tags = ClusterTaggableManager(through=ProductTag, blank=True)

    search_fields = Page.search_fields + [
        index.RelatedFields('tags', [
            index.SearchField('name', partial_match=True, boost=10),
        ]),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        InlinePanel('variants', label='Product variants'),
        InlinePanel('images', label='Product images'),
        FieldPanel('tags'),
    ]

    @property
    def first_image(self):
        return self.images.first()

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
    product = ParentalKey(Product, related_name='variants')
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

class ProductImage(Orderable):

    product = ParentalKey(Product, related_name='images')
    image = models.ForeignKey('wagtailimages.Image', on_delete=models.CASCADE, related_name='+')
    caption = models.CharField(blank=True, max_length=255)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption')
    ]
