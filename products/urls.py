from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductList.as_view(), name='index'),
    path('search', views.ProductSearchListView.as_view(), name='search'),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product'),
]
