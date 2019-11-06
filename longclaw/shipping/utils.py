from django.db.models import Q

from longclaw.shipping import models


class InvalidShippingRate(Exception):
    pass


class InvalidShippingCountry(Exception):
    pass


class InvalidShippingDestination(Exception):
    pass


def get_shipping_cost(settings, country_code=None, name=None, basket_id=None, destination=None):
    """Return the shipping cost for a given country code and shipping option (shipping rate name)
    """
    if not country_code and destination:
        country_code = destination.country.pk
        
    shipping_rate = None
    invalid_country = False
    if settings.default_shipping_enabled:
        shipping_rate = {
            "rate": settings.default_shipping_rate,
            "description": "Standard shipping to rest of world",
            "carrier": settings.default_shipping_carrier
        }
    elif not country_code:
        invalid_country = True

    if country_code:
        qrs = models.ShippingRate.objects.filter(countries__in=[country_code], name=name)
        count = qrs.count()
        if count == 1:
            shipping_rate_qrs = qrs[0]
            shipping_rate = {
                "rate": shipping_rate_qrs.rate,
                "description": shipping_rate_qrs.description,
                "carrier": shipping_rate_qrs.carrier}
    
    if basket_id or destination:
        q = Q()
        
        if destination and basket_id:
            q.add(Q(destination=destination, basket_id=basket_id), Q.OR)
        
        if destination:
            q.add(Q(destination=destination, basket_id=''), Q.OR)
        
        if basket_id:
            q.add(Q(destination=None, basket_id=basket_id), Q.OR)
            
        qrs = models.ShippingRate.objects.filter(name=name).filter(q)
        count = qrs.count()
        if count == 1:
            shipping_rate_qrs = qrs[0]
            shipping_rate = {
                "rate": shipping_rate_qrs.rate,
                "description": shipping_rate_qrs.description,
                "carrier": shipping_rate_qrs.carrier}
    
    if not shipping_rate:
        if invalid_country:
            raise InvalidShippingCountry
        raise InvalidShippingRate()
        
    return shipping_rate
