from django import forms
from longclaw.shipping.models import ShippingRate

class CheckoutForm(forms.Form):
    """
    Captures extra info required for checkout
    """
    email = forms.EmailField()
    shipping_option = forms.CharField(widget=forms.Select, required=False)
    different_billing_address = forms.BooleanField(required=False)
    class Media:
        js = ('checkout.js',)

    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)

        shipping_rates = ShippingRate.objects.filter(countries='NZ')
        choices = [(sr.name, sr.name) for sr in shipping_rates]
        self.fields['shipping_option'].widget.choices = [(sr.name, sr.name) for sr in shipping_rates]
