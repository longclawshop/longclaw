from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.views.decorators.http import require_GET
from django.http import HttpResponseRedirect

try:
  from django.urls import reverse
except ImportError:
  from django.core.urlresolvers import reverse

from longclaw.longclawshipping.forms import AddressForm
from longclaw.longclawcheckout.forms import CheckoutForm
from longclaw.longclawcheckout.utils import create_order
from longclaw.longclawbasket.utils import get_basket_items
from longclaw.longclaworders.models import Order

@require_GET
def checkout_success(request, pk):
    order = get_object_or_404(Order, id=pk)
    return render(request, "longclawcheckout/success.html", { 'order': order })

class CheckoutView(TemplateView):
    template_name = "longclawcheckout/checkout.html"
    checkout_form = CheckoutForm
    shipping_address_form = AddressForm
    billing_address_form = AddressForm

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        items, _ = get_basket_items(self.request)
        total_price = sum(item.total() for item in items)
        context['checkout_form'] = self.checkout_form()
        context['shipping_form'] = self.shipping_address_form(prefix='shipping',
                                                              site=self.request.site)
        context['billing_form'] = self.billing_address_form(prefix='billing',
                                                            site=self.request.site)
        context['basket'] = items
        context['total_price'] = total_price
        return context

    def post(self, request, *args, **kwargs):
        checkout_form = CheckoutForm(request.POST)
        shipping_form = AddressForm(request.POST, prefix='shipping', site=request.site)
        all_ok = checkout_form.is_valid() and shipping_form.is_valid()
        if all_ok:
            email = checkout_form.cleaned_data["email"]
            shipping_option = checkout_form.cleaned_data["shipping_option"]
            shipping_address = shipping_form.save()

            if not checkout_form.cleaned_data["billing_address_is_shipping"]:
                billing_form = AddressForm(request.POST, prefix='billing', site=request.site)
                all_ok = billing_form.is_valid()
                if all_ok:
                    billing_address = billing_form.save()
            else:
                billing_address = shipping_address

        if all_ok:
            order = create_order(
                email,
                request,
                shipping_address=shipping_address,
                billing_address=billing_address,
                shipping_option=shipping_option,
                capture_payment=True
            )
            return HttpResponseRedirect(reverse(
                'longclaw_checkout_success',
                kwargs={'order': order.id}))
