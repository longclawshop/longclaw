import hashlib
import json

from django.core.cache import cache
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models, transaction

# if DJANGO_VERSION < (4, 0):
#     from django.utils.encoding import force_text as force_str
# else:
from django.utils.encoding import force_bytes, force_str
from polymorphic.models import PolymorphicModel

from longclaw.basket.models import BasketItem

from ..serializers.locations import AddressSerializer

# from django import VERSION as DJANGO_VERSION


class ShippingRateProcessor(PolymorphicModel):
    countries = models.ManyToManyField("longclaw_shipping.Country")

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
        from longclaw.basket.serializers import BasketItemSerializer

        settings = kwargs["settings"]
        origin = settings.shipping_origin
        destination = kwargs["destination"]
        basket_id = kwargs["basket_id"]

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
            separators=(",", ": "),
            cls=DjangoJSONEncoder,
        )

        hashed_key = hashlib.sha1(force_bytes(raw_key)).hexdigest()

        return force_str(hashed_key)

    def process_rates(self, **kwargs):
        raise NotImplementedError()
