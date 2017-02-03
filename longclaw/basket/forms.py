from django import forms


class AddToBasketForm(forms.Form):
    quantity = forms.IntegerField()
    product_slug = forms.CharField(widget=forms.HiddenInput())
    variant_ref = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, request=None, *args, **kwargs):
        self.request=request
        super(AddToBasketForm, self).__init__(*args, **kwargs)

    def clean(self):
        ''' Check user has cookies enabled
        '''
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError("Cookies must be enabled.")
        return self.cleaned_data
