from django.db import models
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel

class Address(models.Model):
    name = models.CharField(max_length=64)
    line_1 = models.CharField(max_length=128)
    line_2 = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=64)
    postcode = models.CharField(max_length=10)
    country = models.CharField(max_length=32)

    panels = [
        FieldPanel('name'),
        FieldPanel('line_1'),
        FieldPanel('line_2'),
        FieldPanel('city'),
        FieldPanel('postcode'),
        FieldPanel('country')
    ]

    def __str__(self):
        return "{}, {}, {}".format(self.name, self.city, self.country)

class ShippingCountry(models.Model):
    ''' Standard and premimum rate shipping for
    individual countries.
    '''
    country_code = models.CharField(max_length=3, primary_key=True)
    country_name = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = "shipping countries"

class ShippingRate(models.Model):

    name = models.CharField(max_length=32)
    rate = models.DecimalField(max_digits=12, decimal_places=2)
    carrier = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    shipping_country = models.ForeignKey(ShippingCountry, related_name="shipping_rates")

