from longclaw.longclawshipping import models


class InvalidShippingRate(Exception):
    pass

class InvalidShippingCountry(Exception):
    pass

def get_shipping_cost(country_code, option, settings):
    try:
        qrs = models.ShippingRate.objects.filter(countries__contains=country_code)
        try:
            if qrs.count() > 1:
                shipping_rate = qrs.filter(name=option)[0]
            else:
                shipping_rate = qrs[0]
            return {
                "rate": shipping_rate.rate,
                "description": shipping_rate.description,
                "carrier": shipping_rate.carrier
            }
        except models.ShippingRate.DoesNotExist:
            raise InvalidShippingRate

    except models.ShippingRate.DoesNotExist:
        if settings.default_shipping_enabled:
            return {"rate": settings.default_shipping_rate,
                    "description": "Standard shipping to rest of world",
                    "carrier": settings.default_shipping_rate}
        else:
            raise InvalidShippingCountry
