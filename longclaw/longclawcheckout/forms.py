from django import forms

class CheckoutForm(forms.Form):
    '''
    Captures extra info required for checkout
    '''
    email = forms.EmailField()
    shipping_option = forms.ChoiceField(required=False)
    different_billing_address = forms.BooleanField(required=False)
    class Media:
        js = ('checkout.js',)
