from django.shortcuts import render
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Product


class ProductList(ListView):
    """Return list of Products"""
    template_name = 'index.html'
    queryset = Product.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'List of products'

        return context


class ProductDetailView(DetailView):
    """Return detail of product"""
    model = Product
    template_name = 'product/product.html'


class ProductSearchListView(ListView):
    """Return the list of products searched"""
    template_name = 'product/search.html'

    def get_queryset(self):
        filters = Q(title__icontains=self.query()) |\
            Q(category__title__icontains=self.query())
        return Product.objects.filter(filters)

    def query(self):
        return self.request.GET.get('q')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query()
        context['count'] = context['product_list'].count()

        return context
