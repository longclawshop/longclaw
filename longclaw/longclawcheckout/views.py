from django.shortcuts import render
from django.views.generic.edit import FormView
from django.forms import formset_factory

from longclaw.longclawbasket import utils
from longclaw.longclawshipping.forms import AddressForm
from longclaw.longclawcheckout.forms import CheckoutForm

# Create your views here.
class CheckoutView(FormView):
    template_name = "longclawcheckout/checkout.html"
    form_class = CheckoutForm
    shipping_address_form = AddressForm
    billing_address_form = AddressForm

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        items, _ = utils.get_basket_items(self.request)
        total_price = sum(item.total() for item in items)
        context['shipping_form'] = self.shipping_address_form()
        context['billing_form'] = self.billing_address_form()
        context['basket'] = items
        context['total_price'] = total_price
        return context

    def post(self, request, *args, **kwargs):
        checkout_form = CheckoutForm(request.POST)
        shipping_form = AddressForm(request.POST) 

