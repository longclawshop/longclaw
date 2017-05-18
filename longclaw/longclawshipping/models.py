from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailsnippets.models import register_snippet

@register_snippet
@python_2_unicode_compatible
class Address(models.Model):
    name = models.CharField(max_length=64)
    line_1 = models.CharField(max_length=128)
    line_2 = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=64)
    postcode = models.CharField(max_length=10)
    country = models.ForeignKey('longclawshipping.Country', blank=True, null=True)

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

@python_2_unicode_compatible
class ShippingRate(models.Model):
    '''
    An individual shipping rate. This can be applied to
    multiple countries.
    '''
    name = models.CharField(
        max_length=32,
        unique=True,
        help_text="Unique name to refer to this shipping rate by"
    )
    rate = models.DecimalField(max_digits=12, decimal_places=2)
    carrier = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    countries = models.ManyToManyField('longclawshipping.Country')

    panels = [
        FieldPanel('name'),
        FieldPanel('rate'),
        FieldPanel('carrier'),
        FieldPanel('description'),
        FieldPanel('countries')
    ]

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Country(models.Model):
    """
    International Organization for Standardization (ISO) 3166-1 Country list
    Instance Variables:
    iso -- ISO 3166-1 alpha-2
    name -- Official country names (in all caps) used by the ISO 3166
    display_name -- Country names in title format
    sort_priority -- field that allows for customizing the default ordering
    0 is the default value, and the higher the value the closer to the
    beginning of the list it will be.  An example use case would be you will
    primarily have addresses for one country, so you want that particular
    country to be the first option in an html dropdown box.  To do this, you
    would simply change the value in the json file or alter
    country_grabber.py's priority dictionary and run it to regenerate
    the json
    """
    iso = models.CharField(max_length=2, primary_key=True)
    name_official = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    sort_priority = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Countries'
        ordering = ('-sort_priority', 'name',)

    def __str__(self):
        ''' Return the display form of the country name'''
        return self.name
