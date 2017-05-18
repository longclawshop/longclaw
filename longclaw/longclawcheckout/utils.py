from django.utils.module_loading import import_string

from ipware.ip import get_real_ip

from longclaw.longclaworders.models import Order, OrderItem
from longclaw.longclawshipping.models import Address
from longclaw import settings

GATEWAY = import_string(settings.PAYMENT_GATEWAY)()

def create_order(basket_items,
                 addresses,
                 email,
                 shipping_rate,
                 request):
    '''
    Create an order from a basket and customer infomation
    '''
    if isinstance(addresses, dict):

        # Longclaw < 0.2 used 'shipping_name', longclaw > 0.2 uses a consistent
        # prefix (shipping_address_xxxx)
        try:
            shipping_name = addresses['shipping_name']
        except KeyError:
            shipping_name = addresses['shipping_address_name']

        shipping_country = addresses['shipping_address_country']
        if not shipping_country:
            shipping_country = None
        shipping_address, _ = Address.objects.get_or_create(name=shipping_name,
                                                            line_1=addresses[
                                                                'shipping_address_line1'],
                                                            city=addresses[
                                                                'shipping_address_city'],
                                                            postcode=addresses[
                                                                'shipping_address_zip'],
                                                            country=shipping_country)
        shipping_address.save()
        try:
            billing_name = addresses['billing_name']
        except KeyError:
            billing_name = addresses['billing_address_name']
        billing_country = addresses['shipping_address_country']
        if not billing_country:
            billing_country = None
        billing_address, _ = Address.objects.get_or_create(name=billing_name,
                                                           line_1=addresses[
                                                               'billing_address_line1'],
                                                           city=addresses[
                                                               'billing_address_city'],
                                                           postcode=addresses[
                                                               'billing_address_zip'],
                                                           country=billing_country)
        billing_address.save()

    ip_address = get_real_ip(request)
    order = Order(
        email=email,
        ip_address=ip_address,
        shipping_address=shipping_address,
        billing_address=billing_address,
        shipping_rate=shipping_rate
    )
    order.save()
    # Create the order items
    for item in basket_items:
        order_item = OrderItem(
            product=item.variant,
            quantity=item.quantity,
            order=order
        )
        order_item.save()

    return order
