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
        shipping_address, _ = Address.objects.get_or_create(name=addresses['shipping_name'],
                                                            line_1=addresses[
                                                                'shipping_address_line1'],
                                                            city=addresses[
                                                                'shipping_address_city'],
                                                            postcode=addresses[
                                                                'shipping_address_zip'],
                                                            country=addresses[
                                                                'shipping_address_country'])
        shipping_address.save()
        billing_address, _ = Address.objects.get_or_create(name=addresses['billing_name'],
                                                           line_1=addresses[
                                                               'billing_address_line1'],
                                                           city=addresses[
                                                               'billing_address_city'],
                                                           postcode=addresses[
                                                               'billing_address_zip'],
                                                           country=addresses[
                                                               'billing_address_country'])
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
