from longclaw.longclawshipping import models


class InvalidShippingRate(Exception):
    pass


class InvalidShippingCountry(Exception):
    pass


def get_shipping_cost(country_code, name, settings):
    """
    Return the shipping cost for a given country code and shipping option (shipping rate name)
    """
    qrs = models.ShippingRate.objects.filter(countries__in=[country_code])
    count = qrs.count()
    if count == 1:
        shipping_rate_qrs = qrs[0]
        shipping_rate = {
            "rate": shipping_rate_qrs.rate,
            "description": shipping_rate_qrs.description,
            "carrier": shipping_rate_qrs.carrier}
    elif count > 1:
        qrs = qrs.filter(name=name)
        if qrs.count() == 1:
            shipping_rate_qrs = qrs[0]
            shipping_rate = {
                "rate": shipping_rate_qrs.rate,
                "description": shipping_rate_qrs.description,
                "carrier": shipping_rate_qrs.carrier}
        else:
            raise InvalidShippingRate()
    else:
        if settings.default_shipping_enabled:
            shipping_rate = {
                "rate": settings.default_shipping_rate,
                "description": "Standard shipping to rest of world",
                "carrier": settings.default_shipping_carrier}

        else:
            raise InvalidShippingCountry
    return shipping_rate
