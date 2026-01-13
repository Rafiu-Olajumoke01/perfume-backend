from django.urls import path
from .views import signup, login, get_user, update_user, delete_user, forgot_password, reset_password

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('<int:user_id>/', get_user, name='get_user'),
    path('<int:user_id>/update/', update_user, name='update_user'),
    path('<int:user_id>/delete/', delete_user, name='delete_user'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/', reset_password, name='reset_password'),
]