from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from products.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(['GET'])
def all_orders(request):
    orders = Order.objects.all().order_by('-created_at')  # newest first
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


# ---------------- Create a new order ----------------
@api_view(['POST'])
def create_order(request):
    # Use logged-in user if available, otherwise None for guest
    user = request.user if request.user.is_authenticated else None

    items_data = request.data.get('items')  # list of {product_id, quantity}
    if not items_data:
        return Response({'error': 'No items provided'}, status=status.HTTP_400_BAD_REQUEST)

    total_amount = 0
    # Guest customer info
    customer_name = request.data.get('customer_name', 'Guest')
    customer_email = request.data.get('customer_email', '')
    customer_phone = request.data.get('customer_phone', '')
    delivery_address = request.data.get('delivery_address', '')

    # Create the order
    order = Order.objects.create(
        user=user,
        total_amount=0,  # temporary
        customer_name=customer_name,
        customer_email=customer_email,
        customer_phone=customer_phone,
        delivery_address=delivery_address,
    )

    # Create order items
    for item in items_data:
        product = get_object_or_404(Product, id=item['product_id'])
        quantity = item.get('quantity', 1)
        price = product.price * quantity
        total_amount += price

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )

    order.total_amount = total_amount
    order.save()

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# ---------------- Get orders of a user ----------------
@api_view(['GET'])
def get_my_orders(request, user_id):
    user = get_object_or_404(User, id=user_id)
    orders = Order.objects.filter(user=user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


# ---------------- Update order ----------------
@api_view(['PUT'])
def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    serializer = OrderSerializer(order, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Order updated successfully'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------- Delete order ----------------
@api_view(['DELETE'])
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    return Response({'message': 'Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
