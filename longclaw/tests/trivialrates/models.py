import hashlib

from django.utils.encoding import force_bytes, force_text
from longclaw.shipping.models import ShippingRateProcessor, ShippingRate
from longclaw.basket.models import BasketItem


class TrivialShippingRateProcessor(ShippingRateProcessor):
    def process_rates(self, **kwargs):
        destination = kwargs['destination']
        basket_id = kwargs['basket_id']
        
        item_count = BasketItem.objects.filter(basket_id=basket_id).count()
        
        rates = []
        
        quotes = []
        
        if 0 < item_count:
            quotes.append((item_count * 2, 'turtle'))
        
        if 1 < item_count:
            quotes.append((item_count * 4, 'rabbit'))
        
        if 2 < item_count:
            quotes.append((item_count * 16, 'cheetah'))
        
        for amount, speed in quotes:
            name = self.get_processed_rate_name(destination, basket_id, speed)
            lookups = dict(name=name)
            values = dict(
                rate=amount,
                carrier='TrivialShippingRateProcessor',
                description='Delivered with {} speed'.format(speed),
                basket_id=basket_id,
                destination=destination,
                processor=self,
            )
            
            rate = ShippingRate.objects.update_or_create(defaults=values, **lookups)
            rates.append(rate)
        
        return rates
    
    def get_processed_rate_name(self, destination, basket_id, speed):
        name_long = 'TrivialShippingRateProcessor-{}-{}-{}'.format(destination.pk, basket_id, speed)
        name = hashlib.md5(force_bytes(name_long)).hexdigest()
        return force_text(name)
