from django import forms

class CheckoutForm(forms.Form):
    '''
    Captures extra info required for checkout
    '''
    email = forms.EmailField()
    shipping_option = forms.ChoiceField()
    billing_address_is_shipping = forms.BooleanField(required=False)
