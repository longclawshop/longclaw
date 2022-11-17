import hashlib

# if DJANGO_VERSION < (4, 0):
#     from django.utils.encoding import force_text as force_str
# else:
from django.utils.encoding import force_bytes, force_str

# from django import VERSION as DJANGO_VERSION
from modelcluster.fields import ParentalKey
from wagtail import VERSION as WAGTAIL_VERSION

if WAGTAIL_VERSION >= (3, 0):
    from wagtail.admin.panels import FieldPanel, InlinePanel
    from wagtail.fields import RichTextField
    from wagtail.models import Page
else:
    from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
    from wagtail.core.fields import RichTextField
    from wagtail.core.models import Page

from longclaw.basket.models import BasketItem
from longclaw.products.models import ProductBase, ProductVariantBase
from longclaw.shipping.models import ShippingRate, ShippingRateProcessor


class HomePage(Page):
    pass


class ProductIndex(Page):
    """Index page for all products"""

    subpage_types = ("Product", "ProductIndex")


class Product(ProductBase):
    parent_page_types = [ProductIndex]
    description = RichTextField()
    content_panels = ProductBase.content_panels + [
        FieldPanel("description"),
        InlinePanel("variants"),
    ]


class ProductVariant(ProductVariantBase):
    """Basic product variant for testing"""

    product = ParentalKey(Product, related_name="variants")
    description = RichTextField()

    @ProductVariantBase.price.getter
    def price(self):
        """Make the price dynamic to check that longclaw works with ``get_price``"""
        return self.base_price * 10


class TrivialShippingRateProcessor(ShippingRateProcessor):
    def process_rates(self, **kwargs):
        destination = kwargs["destination"]
        basket_id = kwargs["basket_id"]

        item_count = BasketItem.objects.filter(basket_id=basket_id).count()

        rates = []

        quotes = []

        if 0 < item_count:
            quotes.append((item_count * 2, "turtle"))

        if 1 < item_count:
            quotes.append((item_count * 4, "rabbit"))

        if 2 < item_count:
            quotes.append((item_count * 16, "cheetah"))

        for amount, speed in quotes:
            name = self.get_processed_rate_name(destination, basket_id, speed)
            lookups = dict(name=name)
            values = dict(
                rate=amount,
                carrier="TrivialShippingRateProcessor",
                description="Delivered with {} speed".format(speed),
                basket_id=basket_id,
                destination=destination,
                processor=self,
            )

            rate = ShippingRate.objects.update_or_create(defaults=values, **lookups)
            rates.append(rate)

        return rates

    def get_processed_rate_name(self, destination, basket_id, speed):
        name_long = "TrivialShippingRateProcessor-{}-{}-{}".format(
            destination.pk, basket_id, speed
        )
        name = hashlib.md5(force_bytes(name_long)).hexdigest()
        return force_str(name)
