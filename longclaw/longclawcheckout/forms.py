from django import forms

class CheckoutForm(forms.Form):
    '''
    Captures extra info required for checkout
    '''
    email = forms.EmailField()
    shipping_option = forms.CharField(widget=forms.HiddenInput())
    payment_token = forms.CharField(widget=forms.HiddenInput())
    billing_address_is_shipping = forms.BooleanField(widget=forms.HiddenInput())
