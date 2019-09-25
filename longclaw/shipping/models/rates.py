from django.db import models
from django.dispatch import receiver

from longclaw.basket.signals import basket_modified
from wagtail.admin.edit_handlers import FieldPanel

from ..signals import address_modified


class ShippingRate(models.Model):
    """
    An individual shipping rate. This can be applied to
    multiple countries.
    """
    name = models.CharField(
        max_length=32,
        unique=True,
        help_text="Unique name to refer to this shipping rate by"
    )
    rate = models.DecimalField(max_digits=12, decimal_places=2)
    carrier = models.CharField(max_length=64)
    description = models.CharField(max_length=128)
    countries = models.ManyToManyField('shipping.Country')
    basket_id = models.CharField(blank=True, db_index=True, max_length=32)
    destination = models.ForeignKey('shipping.Address', blank=True, null=True, on_delete=models.PROTECT)
    processor = models.ForeignKey('shipping.ShippingRateProcessor', blank=True, null=True, on_delete=models.PROTECT)

    panels = [
        FieldPanel('name'),
        FieldPanel('rate'),
        FieldPanel('carrier'),
        FieldPanel('description'),
        FieldPanel('countries')
    ]

    def __str__(self):
        return self.name


@receiver(address_modified)
def clear_address_rates(sender, instance, **kwargs):
    ShippingRate.objects.filter(destination=instance).delete()


@receiver(basket_modified)
def clear_basket_rates(sender, basket_id, **kwargs):
    ShippingRate.objects.filter(basket_id=basket_id).delete()
