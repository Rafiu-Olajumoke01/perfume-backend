from django.urls import path
from .views import create_order, get_my_orders, update_order, delete_order, all_orders

urlpatterns = [
    path('orders/', all_orders, name='all-orders'),
    path('create/', create_order, name='create-order'),
    path('my/<int:user_id>/', get_my_orders, name='my-orders'),
    path('update/<int:order_id>/', update_order, name='update-order'), 
    path('delete/<int:order_id>/', delete_order, name='delete-order'),
]