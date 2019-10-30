from rest_framework import serializers

from longclaw.shipping.models.rates import ShippingRate

class ShippingRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingRate
        fields = "__all__"
