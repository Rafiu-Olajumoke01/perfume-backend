from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

# ✅ GET all products safely
@api_view(['GET'])
def get_products(request):
    try:
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    except Exception as e:
        print("Error fetching products:", e)  # Logs error in server console
        return Response(
            {"error": "Failed to fetch products"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# ✅ Add a product (handles image upload)
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def add_product(request):
    try:
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print("Error adding product:", e)
        return Response(
            {"error": "Failed to add product"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# ✅ Get, update, delete a product (handles image upload on PUT)
@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser, FormParser])
def product_detail(request, pk):
    try:
        product = get_object_or_404(Product, pk=pk)

        if request.method == 'GET':
            serializer = ProductSerializer(product)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Product updated successfully'})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            product.delete()
            return Response({'message': 'Product deleted successfully'})

    except Exception as e:
        print(f"Error in product_detail (pk={pk}):", e)
        return Response(
            {"error": "Failed to process product request"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
