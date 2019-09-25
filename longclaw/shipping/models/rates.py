import json
import hashlib

from django.utils.encoding import force_bytes, force_text
from django.core.cache import cache
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models, transaction
from django.dispatch import receiver

from longclaw.basket.models import BasketItem
from longclaw.basket.serializers import BasketItemSerializer
from longclaw.basket.signals import basket_modified
from polymorphic.models import PolymorphicModel
from wagtail.admin.edit_handlers import FieldPanel

from ..serializers import AddressSerializer
from ..signals import address_modified


@receiver(address_modified)
def clear_address_rates(sender, instance, **kwargs):
    ShippingRate.objects.filter(destination=instance).delete()


class ShippingRateProcessor(PolymorphicModel):
    countries = models.ManyToManyField('shipping.Country')
    
    rates_cache_timeout = 300
    def get_rates(self, settings=None, basket_id=None, destination=None):
        kwargs = dict(settings=settings, basket_id=basket_id, destination=destination)
        key = self.get_rates_cache_key(**kwargs)
        rates = cache.get(key)
        if rates is None:
            with transaction.atomic():
                rates = self.process_rates(**kwargs)
            if rates is not None:
                cache.set(key, rates, self.rates_cache_timeout)
        return rates
    
    def get_rates_cache_key(self, **kwargs):
        settings = kwargs['settings']
        origin = settings.shipping_origin
        destination = kwargs['destination']
        basket_id = kwargs['basket_id']
        
        items = BasketItem.objects.filter(basket_id=basket_id)
        serialized_items = BasketItemSerializer(items, many=True)
        
        serialized_origin = AddressSerializer(origin) or None
        serialized_destination = AddressSerializer(destination) or None
        
        data = {
            "items": serialized_items.data,
            "origin": serialized_origin.data,
            "destination": serialized_destination.data,
        }
        
        raw_key = json.dumps(
            data,
            sort_keys=True,
            indent=4,
            separators=(',', ': '),
            cls=DjangoJSONEncoder,
        )
        
        hashed_key = hashlib.sha1(force_bytes(raw_key)).hexdigest()
        
        return force_text(hashed_key)
    
    def process_rates(self, **kwargs):
        raise NotImplementedError()


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
    destination = models.ForeignKey(Address, blank=True, null=True, on_delete=models.PROTECT)
    processor = models.ForeignKey(ShippingRateProcessor, blank=True, null=True, on_delete=models.PROTECT)

    panels = [
        FieldPanel('name'),
        FieldPanel('rate'),
        FieldPanel('carrier'),
        FieldPanel('description'),
        FieldPanel('countries')
    ]

    def __str__(self):
        return self.name


@receiver(basket_modified)
def clear_basket_rates(sender, basket_id, **kwargs):
    ShippingRate.objects.filter(basket_id=basket_id).delete()
