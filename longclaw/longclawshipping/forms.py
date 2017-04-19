from django.forms import ModelForm
from longclaw.longclawshipping.fields import ShippingCountryField
from longclaw.longclawshipping.models import Address

class AddressForm(ModelForm):
    country = ShippingCountryField()
    class Meta:
        model = Address
        fields = ['name', 'line_1', 'line_2', 'city', 'postcode', 'country']
