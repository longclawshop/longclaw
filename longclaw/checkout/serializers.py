from rest_framework import serializers

from longclaw.products.serializers import ProductVariantSerializer
from longclaw.checkout.models import ShippingCountry

class ShippingCountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = ShippingCountry
        fields = "__all__"

    