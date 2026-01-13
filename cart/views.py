from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status 
from .models import CartItem
from .serializers import CartItemSerializer
from django.shortcuts import get_object_or_404
from products.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['GET'])
def get_cart(request, user_id):
    cart_items = CartItem.objects.filter(user_id=user_id)
    serializer = CartItemSerializer(cart_items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_to_cart(request):
    data = request.data
    product = get_object_or_404(Product, id=data.get('product_id'))
    user = get_object_or_404(User, id=data.get('user_id'))

    # First check if cart item exists
    try:
        cart_item = CartItem.objects.get(user=user, product=product)
        cart_item.quantity += data.get('quantity', 1)
    except CartItem.DoesNotExist:
        # If not exists, create it properly with price set
        cart_item = CartItem(
            user=user,
            product=product,
            quantity=data.get('quantity', 1),
            price=product.price
        )

    # Save the cart item
    cart_item.save()

    serializer = CartItemSerializer(cart_item)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def update_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    quantity = request.data.get('quantity')
    if quantity:
        cart_item.quantity = quantity
        cart_item.save()
    serializer = CartItemSerializer(cart_item)
    return Response(serializer.data)

def delete_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return Response({'message': 'Cart item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)