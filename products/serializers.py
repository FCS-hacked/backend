from rest_framework import serializers

from products.models import Product, OrderItem, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'stock', 'image_url')


class OrderItemSerializer(serializers.ModelSerializer):
    product_detailed = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'quantity', 'order', 'product_detailed')


class OrderSerializer(serializers.ModelSerializer):
    items_detailed = OrderItemSerializer(many=True, source='items')

    class Meta:
        model = Order
        fields = ('id', 'status', 'pharmacy', 'buyer', 'price', 'items_detailed')
