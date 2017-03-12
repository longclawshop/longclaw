from django.db import models
from django import forms
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from django_countries.fields import CountryField


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

class ShippingRate(models.Model):
    '''
    An individual shipping rate. This can be applied to
    multiple countries.
    '''
    name = models.CharField(max_length=32, unique=True)
    rate = models.DecimalField(max_digits=12, decimal_places=2)
    carrier = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    countries = CountryField(multiple=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('rate'),
        FieldPanel('carrier'),
        FieldPanel('description'),
        FieldPanel('countries')
    ]

    def __str__(self):
        return self.name
