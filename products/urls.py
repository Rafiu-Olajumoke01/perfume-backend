from django.urls import path
from .views import get_products, add_product, product_detail

urlpatterns = [
    path('', get_products, name='get_products'),
    path('add/', add_product, name='add_product'),
    path('<int:pk>/', product_detail, name='product_detail'),
]
