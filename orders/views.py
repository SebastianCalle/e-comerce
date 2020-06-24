from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from carts.utils import get_or_create_cart
from .utils import get_or_create_order, breadcrumb

from .models import Order

# Create your views here.
@login_required(login_url='login')
def order(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)

    context = {
        'cart': cart,
        'order': order,
        'breadcrumb': breadcrumb,
    }
    return render(request, 'orders/order.html', context)

@login_required(login_url='login')
def address(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)
    shipping_address = order.get_or_set_shipping_address()

    context = {
        'cart': cart,
        'order': order,
        'shipping_address': shipping_address,
        'breadcrumb': breadcrumb(address=True)
    }
    return render(request, 'orders/address.html', context)
