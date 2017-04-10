from rest_framework import serializers
from django_countries.serializer_fields import CountryField

from longclaw.longclawshipping.models import Address, ShippingRate

class AddressSerializer(serializers.ModelSerializer):
    country = CountryField()

    class Meta:
        model = Address
        fields = "__all__"

class ShippingRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShippingRate
        fields = "__all__"

    