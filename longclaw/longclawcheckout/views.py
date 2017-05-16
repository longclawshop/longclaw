from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect

from longclaw.longclawbasket import utils
from longclaw.longclawshipping.forms import AddressForm
from longclaw.longclawcheckout.forms import CheckoutForm


class CheckoutView(TemplateView):
    template_name = "longclawcheckout/checkout.html"
    checkout_form = CheckoutForm
    shipping_address_form = AddressForm
    billing_address_form = AddressForm

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        items, _ = utils.get_basket_items(self.request)
        total_price = sum(item.total() for item in items)
        context['checkout_form'] = self.checkout_form()
        context['shipping_form'] = self.shipping_address_form(prefix='shipping')
        context['billing_form'] = self.billing_address_form(prefix='billing')
        context['basket'] = items
        context['total_price'] = total_price
        return context

    def post(self, request, *args, **kwargs):
        checkout_form = CheckoutForm(request.POST)
        shipping_form = AddressForm(request.POST, prefix='shipping')
        all_ok = checkout_form.is_valid() and shipping_form.is_valid()
        if all_ok:
            email = checkout_form.cleaned_data["email"]
            shipping_address = shipping_form.save()

            if not checkout_form.cleaned_data["billing_address_is_shipping"]:
                billing_form = AddressForm(request.POST, prefix='billing')
                all_ok = billing_form.is_valid()
                if all_ok:
                    billing_address = billing_form.save()
            else:
                billing_address = shipping_address

        if all_ok:
            return HttpResponseRedirect('/thanks/')


