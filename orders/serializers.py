from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

# ---------------- Order Item Serializer ----------------
class OrderItemSerializer(serializers.ModelSerializer):
    # Include product details for frontend
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']


# ---------------- Order Serializer ----------------
class OrderSerializer(serializers.ModelSerializer):
    # Include all items in the order
    items = OrderItemSerializer(many=True, read_only=True)
    # Show user's email
    user = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_amount', 'status', 'items', 'created_at']
