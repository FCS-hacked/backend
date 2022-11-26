from rest_framework import serializers

from authentication.serializers import OrganizationExternalSerializer
from products.models import Product, OrderItem, Order, InsuranceClaim


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
        fields = ('id', 'status', 'pharmacy', 'buyer', 'price', 'items_detailed', 'prescription', 'invoice')


class InsuranceClaimSerializer(serializers.ModelSerializer):
    provider_detailed = OrganizationExternalSerializer(source='provider', read_only=True)
    order_detailed = OrderSerializer(source='order', read_only=True)

    class Meta:
        model = InsuranceClaim
        fields = ('id', 'status', 'provider_detailed', 'order_detailed',)
