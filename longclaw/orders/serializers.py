from rest_framework import serializers
from longclaw.orders.models import Order, OrderItem
from longclaw.coupon.models import Discount
from longclaw.coupon.utils import discount_total
from longclaw.products.serializers import ProductVariantSerializer
from longclaw.shipping.serializers import AddressSerializer

class OrderItemSerializer(serializers.ModelSerializer):

    product = ProductVariantSerializer()

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True)
    shipping_address = AddressSerializer()
    total = serializers.SerializerMethodField()

    def to_representation(self, value):
        rep = super().to_representation(value)
        try:
            discount = Discount.objects.get(order=value.id)
            rep['discount_total'], amount_off = discount_total(value.total + value.shipping_rate, discount)
            rep['discount_value'] = discount.coupon.discount_string(discount.coupon.discount_value)
        except Discount.DoesNotExist:
            pass
            
        return rep

    class Meta:
        model = Order
        fields = "__all__"

    def get_total(self, obj):
        return obj.total
