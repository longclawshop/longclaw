from longclaw.longclawsettings.models import LongclawSettings
from longclaw.longclawshipping.models import ShippingRate
from django_countries import countries, fields

class CountryChoices(object):
    '''
    Helper class which returns a list of available countries based on
    the selected shipping options.

    If default_shipping_enabled is ``True`` in the longclaw settings, then
    all possible countries are returned. Otherwise only countries for
    which a ``ShippingRate`` has been declared are returned.
    '''
    def __init__(self, **kwargs):
        request = kwargs.get('request', None)
        self._all_countries = True
        if request:
            settings = LongclawSettings.for_site(request.site)
            self._all_countries = settings.default_shipping_enabled

    def __call__(self, *args, **kwargs):
        if self._all_countries:
            return countries
        else:
            return ShippingRate.objects.values_list('countries').distinct()


class ShippingCountryField(fields.CountryField):
    '''
    Country choice field whose choices are constrained by the
    configured shipping options.
    '''
    def __init__(self, *args, **kwargs):
        kwargs.update({
            'countries': CountryChoices(**kwargs)
        })
        super(ShippingCountryField, self).__init__(*args, **kwargs)

