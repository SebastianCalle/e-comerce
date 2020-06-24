from django.shortcuts import render
from .models import Cart
from .utils import get_or_create_cart
from products.models import Product
from django.shortcuts import redirect, get_object_or_404
from .models import CartProducts

def cart(request):
    """Cart view"""
    cart = get_or_create_cart(request)
    context = {'cart': cart,}

    return render(request, 'carts/cart.html', context)

def add(request):
    cart = get_or_create_cart(request)
    product = Product.objects.filter(pk=request.POST.get('product_id')).first()
    quantity = int(request.POST.get('quantity', 1))

    cart_product = CartProducts.objects.create_or_update_quantity(cart=cart,
                                                                  product=product,
                                                                  quantity=quantity)
    #cart.products.add(product, through_defaults={'quantity': quantity})

    context = { 'product': product, 'quantity': quantity }

    return render(request, 'carts/add.html', context)

def remove(request):
    cart = get_or_create_cart(request)
    #product = Product.objects.filter(pk=request.POST.get('product_id')).first()
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))

    cart.products.remove(product)

    return redirect('carts:cart')
