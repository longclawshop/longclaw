from django import forms

class CheckoutForm(forms.Form):
    '''
    Captures extra info required for checkout
    '''
    email = forms.EmailField()
    shipping = forms.FloatField(widget=forms.HiddenInput())
