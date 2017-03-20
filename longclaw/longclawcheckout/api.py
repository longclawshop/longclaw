'''
Shipping logic and payment capture API
'''
from django.utils import timezone
from django.utils.module_loading import import_string
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from longclaw.longclawbasket.utils import get_basket_items, destroy_basket
from longclaw.longclawcheckout.utils import PaymentError, create_order
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
def create_order_with_token(request):
    '''
    Create an order using an existing transaction ID.
    This is useful for capturing the payment outside of
    longclaw - e.g. using paypals' express checkout or
    similar
    '''
    # Get the request data
    try:
        address = request.data['address']
        postage = float(request.data['shipping_rate'])
        email = request.data['email']
        transaction_id = request.data['transaction_id']
    except KeyError:
        return Response(data={"message": "Missing parameters from request data"},
                        status=status.HTTP_400_BAD_REQUEST)

    # Get the contents of the basket
    items, _ = get_basket_items(request)
    # Create the order
    ip_address = request.data.get('ip', '0.0.0.0')
    order = create_order(
        items,
        address,
        email,
        postage,
        ip_address
    )

    order.payment_date = timezone.now()
    order.transaction_id = transaction_id
    order.save()
    # Once the order has been successfully taken, we can empty the basket
    destroy_basket(request)

    return Response(data={"order_id": order.id}, status=status.HTTP_201_CREATED)

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

    # Create the order
    address = request.data['address']
    postage = float(request.data['shipping_rate'])
    email = request.data['email']
    ip_address = request.data.get('ip', '0.0.0.0')
    order = create_order(
        items,
        address,
        email,
        postage,
        ip_address
    )

    # Capture the payment
    try:
        desc = 'Payment from {} for order id #{}'.format(request.data['email'], order.id)
        transaction_id = gateway.create_payment(request,
                                                float(total) + postage,
                                                description=desc)
        order.payment_date = timezone.now()
        order.transaction_id = transaction_id
        # Once the order has been successfully taken, we can empty the basket
        destroy_basket(request)
        response = Response(data={"order_id": order.id},
                            status=status.HTTP_201_CREATED)
    except PaymentError as err:
        order.status = Order.CANCELLED
        order.note = "Payment failed"
        response = Response(data={"message": err.message, "order_id": order.id},
                            status=status.HTTP_400_BAD_REQUEST)
    order.save()
    return response
