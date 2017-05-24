from django.forms import ModelForm, ModelChoiceField
from longclaw.longclawsettings.models import LongclawSettings
from longclaw.longclawshipping.models import Address, Country

class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'line_1', 'line_2', 'city', 'postcode', 'country']

    def __init__(self, *args, **kwargs):
        site = kwargs.pop('site', None)
        super(AddressForm, self).__init__(*args, **kwargs)

        # Edit the country field to only contain
        # countries specified for shipping
        all_countries = True
        if site:
            settings = LongclawSettings.for_site(site)
            all_countries = settings.default_shipping_enabled
        if all_countries:
            queryset = Country.objects.all()
        else:
            queryset = Country.objects.exclude(shippingrate=None)
        self.fields['country'] = ModelChoiceField(queryset)

