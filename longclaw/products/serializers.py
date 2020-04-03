from rest_framework import serializers
from longclaw.utils import ProductVariant, maybe_get_product_model

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = maybe_get_product_model()
        fields = "__all__"


class ProductVariantSerializer(serializers.ModelSerializer):

    if maybe_get_product_model():
        product = ProductSerializer()

    class Meta:
        model = ProductVariant
        fields = "__all__"
