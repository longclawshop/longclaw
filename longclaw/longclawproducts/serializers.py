from rest_framework import serializers
from longclaw.longclawproducts.models import Product
from longclaw.utils import ProductVariant

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


class ProductVariantSerializer(serializers.ModelSerializer):

    product = ProductSerializer()

    class Meta:
        model = ProductVariant
        fields = "__all__"
