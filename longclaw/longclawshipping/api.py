from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from longclaw.longclawshipping import models, utils
from longclaw.longclawsettings.models import LongclawSettings


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

    option = request.query_params.get('shipping_rate_name', 'standard')
    try:
        settings = LongclawSettings.for_site(request.site)
        data = utils.get_shipping_cost(code, option, settings)
        response = Response(data=data, status=status.HTTP_200_OK)
    except utils.InvalidShippingRate:
        response = Response(data={"message": "Shipping option {} is invalid".format(option)},
                            status=status.HTTP_400_BAD_REQUEST)
    except utils.InvalidShippingCountry:
        response = Response(data={"message": "Shipping to {} is not available".format(code)},
                            status=status.HTTP_400_BAD_REQUEST)

    return response


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def shipping_countries(request):
    ''' Get all shipping countries
    '''
    queryset = models.ShippingRate.objects.all()
    country_data = [(c.name, c.code) for obj in queryset for c in obj.countries]
    return Response(data=country_data, status=status.HTTP_200_OK)
