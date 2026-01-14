from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse  

# Simpler root view
def api_root(request):
    return HttpResponse("API is running. Try /api/products/ or /api/orders/orders/")

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    
    # ---------------- API endpoints ----------------
    path('api/products/', include('products.urls')),   
    path('api/users/', include('users.urls')),      
    path('api/orders/', include('orders.urls')),       
    path('api/cart/', include('cart.urls')),         
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)