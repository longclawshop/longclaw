from django.apps import apps
from rest_framework import serializers
from longclaw.orders.models import Order, OrderItem
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

    class Meta:
        model = Order
        fields = "__all__"

    def get_total(self, obj):
      return obj.total
