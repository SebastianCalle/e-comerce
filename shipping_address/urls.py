from django.urls import path

from . import views

app_name = 'shipping_address'

urlpatterns = [
    path('', views.ShippingAddressListView.as_view(), name='shipping_address'),
    path('update/<int:pk>', views.ShippingAddressUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', views.ShippingAdressDeleteView.as_view(), name='delete'),
    path('default/<int:pk>', views.default, name='default'),
    path('create/', views.create, name='create')
]
