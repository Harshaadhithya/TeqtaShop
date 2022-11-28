from itertools import product
from rest_framework import serializers
from .models import *
from inventory.models import *


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductVariantSerializer(many=False)
    product_total = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = '__all__'

    def get_product_total(self, obj):
        return obj.get_total


class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    cart_total = serializers.SerializerMethodField()
    cart_total_qty = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_order_items(self, obj):
        order_items = obj.orderitem_set.all()
        serialized_order_items = OrderItemSerializer(order_items, many=True).data
        return serialized_order_items

    def get_cart_total(self, obj):
        return obj.get_cart_total

    def get_cart_total_qty(self, obj):
        return obj.get_cart_qty_total
