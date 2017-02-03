'''
Shipping logic and payment capture API
'''
from django.utils.module_loading import import_string
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from longclaw.basket.utils import get_basket_items, destroy_basket
from longclaw.orders.models import Order, OrderItem, Address
from longclaw.checkout.models import ShippingCountry
from longclaw.checkout import app_settings, serializers
from longclaw.checkout.utils import PaymentError

gateway = import_string(app_settings.PAYMENT_GATEWAY)()

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def create_token(request):
    ''' Generic function for creating a payment token from the
    payment backend. Some payment backends (e.g. braintree) support creating a payment
    token, which should be imported from the backend as 'get_token'
    '''
    token = gateway.get_token(request)
    return Response({'token': token}, status=status.HTTP_200_OK)


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
    # Create the order
    order = Order(
        email=request.data['email'],
        ip_address=request.data.get('ip', '0.0.0.0'),
        shipping_address=shipping_address,
        billing_address=billing_address
    )
    order.save()

    # Create the order items
    for item in items:
        order_item = OrderItem(
            product=item.product,
            quantity=item.quantity,
            order=order
        )
        order_item.save()

    postage = float(request.data['shipping_rate'])
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

class InvalidShippingRate(Exception):
    pass

class InvalidShippingCountry(Exception):
    pass

def get_shipping_cost(country_code, option):
    try:
        obj = ShippingCountry.objects.get(country_code=country_code)
        if option == 'standard':
            return {"rate": obj.standard_rate,
                    "description": obj.standard_rate_description,
                    "carrier": obj.standard_rate_carrier}
        elif option == 'premium':
            return {"rate": obj.premium_rate,
                    "description": obj.premium_rate_description,
                    "carrier": obj.premium_rate_carrier}
        else:
            raise InvalidShippingRate

    except ShippingCountry.DoesNotExist:
        if app_settings.DEFAULT_SHIPPING_ENABLED:
            return {"rate": app_settings.DEFAULT_SHIPPING_RATE,
                    "description": "Standard shipping to rest of world",
                    "carrier": app_settings.DEFAULT_SHIPPING_CARRIER}
        else:
            raise InvalidShippingCountry



@api_view(['GET'])
@permission_classes({permissions.AllowAny})
def shipping_cost(request):
    ''' Returns the shipping cost for a given country
    If the shipping cost for the given country has not been set, it will
    fallback to the default shipping cost if it has been enabled in the app
    settings
    '''
    try:
        code = request.query_params.get('country_code')
    except AttributeError:
        return Response(data={"message": "No country code supplied"},
                        status=status.HTTP_400_BAD_REQUEST)

    option = request.query_params.get('shipping_option', 'standard')
    try:
        data = get_shipping_cost(code, option)
        response = Response(data=data, status=status.HTTP_200_OK)
    except InvalidShippingRate:
        response = Response(data={"message": "Shipping option {} is invalid".format(option)},
                            status=status.HTTP_400_BAD_REQUEST)
    except InvalidShippingCountry:
        response = Response(data={"message": "Shipping to {} is not available".format(code)},
                            status=status.HTTP_400_BAD_REQUEST)

    return response


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_shipping_countries(request):
    ''' Get all shipping countries
    '''
    queryset = ShippingCountry.objects.all()
    serializer = serializers.ShippingCountrySerializer(queryset, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
