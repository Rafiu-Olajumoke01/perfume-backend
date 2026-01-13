from django.urls import path
from .views import get_cart, add_to_cart, update_cart_item, delete_cart_item

urlpatterns = [
    # GET cart items for a user
    path('<int:user_id>/', get_cart, name='get_cart'),
    path('add/', add_to_cart, name='add_to_cart'),
    path('<int:cart_item_id>/update/', update_cart_item, name='update_cart_item'),
    path('<int:cart_item_id>/delete/', delete_cart_item, name='delete_cart_item'),
]
