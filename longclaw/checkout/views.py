from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.views.decorators.http import require_GET
from django.http import HttpResponseRedirect

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from longclaw.shipping.forms import AddressForm
from longclaw.checkout.forms import CheckoutForm
from longclaw.checkout.utils import create_order
from longclaw.basket.utils import get_basket_items, basket_id
from longclaw.orders.models import Order
from longclaw.coupon.models import Discount
from longclaw.coupon.utils import discount_total


@require_GET
def checkout_success(request, pk):
    order = get_object_or_404(Order, id=pk)
    return render(request, "checkout/success.html", {'order': order})


class CheckoutView(TemplateView):
    template_name = "checkout/checkout.html"
    checkout_form = CheckoutForm
    shipping_address_form = AddressForm
    billing_address_form = AddressForm

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        items, _ = get_basket_items(self.request)
        total_price = sum(item.total() for item in items)
        discount = Discount.objects.filter(basket_id=basket_id(self.request), order=None).last()
        discount_total_price, discount_total_saved = discount_total(total_price, discount)
        site = getattr(self.request, 'site', None)
        context['checkout_form'] = self.checkout_form(
            self.request.POST or None)
        context['shipping_form'] = self.shipping_address_form(
            self.request.POST or None,
            prefix='shipping',
            site=site)
        context['billing_form'] = self.billing_address_form(
            self.request.POST or None,
            prefix='billing',
            site=site)
        context['basket'] = items
        
        default_shipping_rate = ShippingRate.objects.first().rate
        total_price = sum(item.total() for item in items)
        discount = Discount.objects.filter(basket_id=basket_id(self.request), order=None).last()
        discount_total_price, discount_total_saved = discount_total(total_price + default_shipping_rate, discount)
        context['total_price'] = total_price
        context['discount'] = discount
        context['discount_total_price'] = round(discount_total_price, 2)
        context['discount_total_saved'] = round(discount_total_saved, 2)

        context['default_shipping_rate'] = round(default_shipping_rate, 2)

        context['discount_plus_shipping'] = round(discount_total_price + default_shipping_rate, 2)
        context['total_plus_shipping'] = round(total_price + default_shipping_rate, 2)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        checkout_form = context['checkout_form']
        shipping_form = context['shipping_form']
        discount = context['discount']
        all_ok = checkout_form.is_valid() and shipping_form.is_valid()
        if all_ok:
            email = checkout_form.cleaned_data['email']
            shipping_option = checkout_form.cleaned_data.get(
                'shipping_option', None)
            shipping_address = shipping_form.save()

            if checkout_form.cleaned_data['different_billing_address']:
                billing_form = context['billing_form']
                all_ok = billing_form.is_valid()
                if all_ok:
                    billing_address = billing_form.save()
            else:
                billing_address = shipping_address

        if all_ok:
            try:
                order = create_order(
                    email,
                    request,
                    shipping_address=shipping_address,
                    billing_address=billing_address,
                    shipping_option=shipping_option,
                    delivery_instructions=delivery_instructions,
                    discount=discount,
                    capture_payment=True
                )
            except ValueError: 
                # Something went wrong, no items in basket?
                return super(CheckoutView, self).render_to_response(context)
            else:
                # Check for if the payment went through
                if order.status == order.SUBMITTED:
                    return HttpResponseRedirect(reverse(
                        'longclaw_checkout_success',
                        kwargs={'pk': order.id}
                    ))
                else:
                    context['checkout_form'] = checkout_form
                    context['shipping_form'] = shipping_form
                    context['discount'] = discount
                    if order.status == order.FAILURE:
                        context['payment_error'] = order.status_note
                    return super(CheckoutView, self).render_to_response(context)
                
        return super(CheckoutView, self).render_to_response(context)
