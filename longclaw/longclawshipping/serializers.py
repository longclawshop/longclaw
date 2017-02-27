from rest_framework import serializers
from longclaw.longclawshipping.models import Address, ShippingRate

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = "__all__"

class ShippingRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShippingRate
        fields = "__all__"

    