from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from longclaw.shipping import serializers, models
from longclaw import settings

class InvalidShippingRate(Exception):
    pass

class InvalidShippingCountry(Exception):
    pass

def get_shipping_cost(country_code, option):
    try:
        obj = models.ShippingCountry.objects.get(country_code=country_code)
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

    except models.ShippingCountry.DoesNotExist:
        if settings.DEFAULT_SHIPPING_ENABLED:
            return {"rate": settings.DEFAULT_SHIPPING_RATE,
                    "description": "Standard shipping to rest of world",
                    "carrier": settings.DEFAULT_SHIPPING_CARRIER}
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
def shipping_countries(request):
    ''' Get all shipping countries
    '''
    queryset = models.ShippingCountry.objects.all()
    serializer = serializers.ShippingCountrySerializer(queryset, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
