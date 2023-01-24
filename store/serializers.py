from itertools import product
from rest_framework import serializers
from .models import *
from inventory.models import *




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class VariantImageSerializer(serializers.ModelSerializer):
    image=serializers.SerializerMethodField()
    class Meta:
        model = ProductImage
        fields = '__all__'

    def get_image(self,obj):
        return {'url':obj.image.url}

class ProductVariantSerializer(serializers.ModelSerializer):
    product=ProductSerializer(many=False)
    variant_image=serializers.SerializerMethodField()
    class Meta:
        model = ProductVariant
        fields = '__all__'

    def get_variant_image(self, obj):
        return {'first':VariantImageSerializer(obj.variant_image.first(),many=False).data}

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



class GuestCartSerializer(serializers.Serializer):
    id=serializers.CharField(max_length = 200)
    product=ProductVariantSerializer(many=False)
    quantity=serializers.IntegerField()
    get_total=serializers.DecimalField(max_digits=10, decimal_places=2)
