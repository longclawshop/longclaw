from django.apps import apps
from rest_framework import serializers
from longclaw.products.models import Product
from longclaw.settings import PRODUCT_VARIANT_MODEL

ProductVariant = apps.get_model(*PRODUCT_VARIANT_MODEL.split('.'))

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


class ProductVariantSerializer(serializers.ModelSerializer):

    product = ProductSerializer()

    class Meta:
        model = ProductVariant
        fields = "__all__"
