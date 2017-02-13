'''
Shipping logic and payment capture API
'''
from django.utils.module_loading import import_string
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from longclaw.basket.utils import get_basket_items, destroy_basket
from longclaw.orders.models import Order, OrderItem
from longclaw.shipping.models import Address
from longclaw.checkout.utils import PaymentError
from longclaw import settings

gateway = import_string(settings.PAYMENT_GATEWAY)()

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def create_token(request):
    ''' Generic function for creating a payment token from the
    payment backend. Some payment backends (e.g. braintree) support creating a payment
    token, which should be imported from the backend as 'get_token'
    '''
    token = gateway.get_token(request)
    return Response({'token': token}, status=status.HTTP_200_OK)

@transaction.atomic
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def capture_payment(request):
    '''
    Capture the payment for a basket and create an order

    request.data should contain:

    'address': Dict with the following fields:
        shipping_name
        shipping_address_line1
        shipping_address_city
        shipping_address_zip
        shipping_address_country
        billing_name
        billing_address_line1
        billing_address_city
        billing_address_zip
        billing_address_country

    'email': Email address of the customer
    'ip': IP address of the customer
    'shipping': The shipping rate (standard or premium)
    '''

    # Get the contents of the basket
    items, _ = get_basket_items(request)

    # Compute basket total
    total = 0
    for item in items:
        total += item.total()

    # Create the address for the order
    address = request.data['address']
    shipping_address, _ = Address.objects.get_or_create(name=address['shipping_name'],
                                                        line_1=address['shipping_address_line1'],
                                                        city=address['shipping_address_city'],
                                                        postcode=address['shipping_address_zip'],
                                                        country=address['shipping_address_country'])
    shipping_address.save()

    address = request.data['address']
    billing_address, _ = Address.objects.get_or_create(name=address['billing_name'],
                                                       line_1=address['billing_address_line1'],
                                                       city=address['billing_address_city'],
                                                       postcode=address['billing_address_zip'],
                                                       country=address['billing_address_country'])
    billing_address.save()
    postage = float(request.data['shipping_rate'])
    # Create the order
    order = Order(
        email=request.data['email'],
        ip_address=request.data.get('ip', '0.0.0.0'),
        shipping_address=shipping_address,
        billing_address=billing_address,
        shipping_rate=postage
    )
    order.save()

    # Create the order items
    for item in items:
        order_item = OrderItem(
            product=item.variant,
            quantity=item.quantity,
            order=order
        )
        order_item.save()

    try:
        gateway.create_payment(request, float(total)+postage)
        # Once the order has been successfully taken, we can empty the basket
        destroy_basket(request)
        response = Response(data={"order_id": order.id}, status=status.HTTP_201_CREATED)
    except PaymentError as err:
        order.status = Order.CANCELLED
        order.note = "Payment failed"
        order.save()
        response = Response(data={"message": err.message, "order_id": order.id},
                            status=status.HTTP_400_BAD_REQUEST)
    return response
