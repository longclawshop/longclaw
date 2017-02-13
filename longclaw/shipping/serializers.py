from rest_framework import serializers
from longclaw.shipping.models import Address, ShippingCountry, ShippingRate

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = "__all__"

class ShippingRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShippingRate
        fields = "__all__"

class ShippingCountrySerializer(serializers.ModelSerializer):

    shipping_rates = ShippingRateSerializer(many=True)

    class Meta:
        model = ShippingCountry
        fields = "__all__"

    