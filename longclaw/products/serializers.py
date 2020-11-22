from rest_framework import serializers
from longclaw.utils import ProductVariant, maybe_get_product_model

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = maybe_get_product_model()
        fields = "__all__"


class ProductVariantSerializer(serializers.ModelSerializer):

    product = ProductSerializer()

    def to_representation(self, value):
        rep = super().to_representation(value)
        rep['price'] = value.price
        if value.product.first_image:
            rep['thumbnail'] = value.product.first_image.image.get_rendition('width-200').url
        return rep

    class Meta:
        model = ProductVariant
        fields = "__all__"
