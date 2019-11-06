from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from longclaw.shipping import models, utils, serializers
from longclaw.configuration.models import Configuration
from longclaw.basket.utils import basket_id

from .models import ShippingRateProcessor
from .signals import address_modified

class AddressViewSet(viewsets.ModelViewSet):
    """
    Create, list and view Addresses
    """
    queryset = models.Address.objects.all()
    serializer_class = serializers.AddressSerializer
    
    def perform_create(self, serializer):
        output = super().perform_create(serializer)
        instance = serializer.instance
        address_modified.send(sender=models.Address, instance=instance)
    
    def perform_update(self, serializer):
        output = super().perform_update(serializer)
        instance = serializer.instance
        address_modified.send(sender=models.Address, instance=instance)
    
    def perform_destroy(self, instance):
        output = super().perform_destroy(instance)
        address_modified.send(sender=models.Address, instance=instance)


def get_shipping_cost_kwargs(request, country=None):
    country_code = request.query_params.get('country_code', None)
    if country:
        if country_code is not None:
            raise utils.InvalidShippingCountry("Cannot specify country and country_code")
        country_code = country
    
    destination = request.query_params.get('destination', None)
    if destination:
        try:
            destination = models.Address.objects.get(pk=destination)
        except models.Address.DoesNotExist:
            raise utils.InvalidShippingDestination("Address not found")
    elif not country_code:
        raise utils.InvalidShippingCountry("No country code supplied")
    
    if not country_code:
        country_code = destination.country.pk

    bid = basket_id(request)
    option = request.query_params.get('shipping_rate_name', 'standard')
    settings = Configuration.for_site(request.site)
    
    return dict(country_code=country_code, destination=destination, basket_id=bid, settings=settings, name=option)


@api_view(['GET'])
@permission_classes({permissions.AllowAny})
def shipping_cost(request):
    """ Returns the shipping cost for a given country
    If the shipping cost for the given country has not been set, it will
    fallback to the default shipping cost if it has been enabled in the app
    settings
    """
    status_code = status.HTTP_400_BAD_REQUEST
    try:
        kwargs = get_shipping_cost_kwargs(request)
    except (utils.InvalidShippingCountry, utils.InvalidShippingDestination) as e:
        data = {'message': e.message}
    else:
        try:
            data = utils.get_shipping_cost(**kwargs)
        except utils.InvalidShippingRate:
            data = {
                "message": "Shipping option {} is invalid".format(kwargs['name'])
            }
        except utils.InvalidShippingCountry:
            data = {
                "message": "Shipping to {} is not available".format(kwargs['country_code'])
            }
        else:
            status_code = status.HTTP_200_OK

    return Response(data=data, status=status_code)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def shipping_countries(request):
    """ Get all shipping countries
    """
    queryset = models.Country.objects.exclude(shippingrate=None)
    serializer = serializers.CountrySerializer(queryset, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def shipping_options(request, country=None):
    """
    Get the shipping options for a given country
    """
    try:
        kwargs = get_shipping_cost_kwargs(request, country=country)
    except (utils.InvalidShippingCountry, utils.InvalidShippingDestination) as e:
        return Response(data={'message': e.message}, status=status.HTTP_400_BAD_REQUEST)
    
    country_code = kwargs['country_code']
    settings = kwargs['settings']
    bid = kwargs['basket_id']
    destination = kwargs['destination']
    
    processors = ShippingRateProcessor.objects.filter(countries__in=[country_code])
    if processors:
        if not destination:
            return Response(
                data={
                    "message": "Destination address is required for rates to {}.".format(country_code)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        for processor in processors:
            processor.get_rates(settings=settings, basket_id=bid, destination=destination)
    
    q = Q(countries__in=[country_code]) | Q(basket_id=bid, destination=None)
    
    if destination:
        q.add(Q(destination=destination, basket_id=''), Q.OR)
        q.add(Q(destination=destination, basket_id=bid), Q.OR)
    
    qrs = models.ShippingRate.objects.filter(q)
    serializer = serializers.ShippingRateSerializer(qrs, many=True)
    return Response(
        data=serializer.data,
        status=status.HTTP_200_OK
    )
