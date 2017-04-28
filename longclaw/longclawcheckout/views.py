from django.shortcuts import render
from django.views.generic.edit import FormView
from django.forms import formset_factory

from longclaw.longclawshipping.forms import AddressForm
from longclaw.longclawcheckout.forms import CheckoutForm

# Create your views here.
class CheckoutView(FormView):
    template_name = "longclawcheckout/checkout.html"
    AddressFormSet = formset_factory(AddressForm, max_num=2, min_num=1, extra=0)
    form_class = CheckoutForm

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        context['address_formset'] = self.AddressFormSet()
        return context

    def post(self, request, *args, **kwargs):
        address_formset = self.AddressFormSet(request.POST)
        checkout_form = CheckoutForm(request.POST)

