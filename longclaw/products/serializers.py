from django.conf import settings
from django.apps import apps
from rest_framework import serializers
from longclaw.products.models import Product

PRODUCT_VARIANT_MODEL = getattr(settings, 'PRODUCT_VARIANT_MODEL', 'products.ProductVariant')
ProductVariant = apps.get_model(*PRODUCT_VARIANT_MODEL.split('.'))

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


class ProductVariantSerializer(serializers.ModelSerializer):

    page = ProductSerializer()

    class Meta:
        model = ProductVariant
        fields = "__all__"
