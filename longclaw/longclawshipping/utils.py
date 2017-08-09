from longclaw.longclawshipping import models


class InvalidShippingRate(Exception):
    pass


class InvalidShippingCountry(Exception):
    pass

def get_shipping_cost(settings, country_code=None, name=None):
    """Return the shipping cost for a given country code and shipping option (shipping rate name)
    """
    shipping_rate = None
    if settings.default_shipping_enabled:
        shipping_rate = {
            "rate": settings.default_shipping_rate,
            "description": "Standard shipping to rest of world",
            "carrier": settings.default_shipping_carrier
        }
    elif not country_code:
        raise InvalidShippingCountry

    if country_code:
        qrs = models.ShippingRate.objects.filter(countries__in=[country_code], name=name)
        count = qrs.count()
        if count == 1:
            shipping_rate_qrs = qrs[0]
        else:
            raise InvalidShippingRate()
        shipping_rate = {
            "rate": shipping_rate_qrs.rate,
            "description": shipping_rate_qrs.description,
            "carrier": shipping_rate_qrs.carrier}
    return shipping_rate
