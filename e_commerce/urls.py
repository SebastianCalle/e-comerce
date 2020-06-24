from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls'), name='products'),
    path('cart/', include('carts.urls'), name='carts'),
    path('order/', include('orders.urls'), name='orders'),
    path('directions/', include('shipping_address.urls'),
         name='shipping_addresses'),
    path('users/login/', views.login_view, name='login'),
    path('users/logout/', views.logout_view, name='logout'),
    path('users/register/', views.register_view, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
