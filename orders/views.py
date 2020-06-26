from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from shipping_address.models import ShippingAdress

from carts.utils import get_or_create_cart, destroy_cart
from .utils import get_or_create_order, breadcrumb, destroy_order

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
    can_choose_address = request.user.shippingadress_set.count() > 1

    context = {
        'cart': cart,
        'order': order,
        'shipping_address': shipping_address,
        'breadcrumb': breadcrumb(address=True),
        'can_choose_address': can_choose_address,
    }
    return render(request, 'orders/address.html', context)


@login_required(login_url='login')
def select_address(request):
    shipping_address = request.user.shippingadress_set.all()
    context = {
        'breadcrumb': breadcrumb(address=True),
        'shipping_address': shipping_address,
    }
    return render(request, 'orders/select_address.html', context)


@login_required(login_url='login')
def check_address(request, pk):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)

    shipping_address = get_object_or_404(ShippingAdress, pk=pk)

    if request.user.id != shipping_address.user_id:
        return redirect('carts:cart')

    order.update_shipping_address(shipping_address)

    return redirect('orders:address')


@login_required(login_url='login')
def confirm(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)

    shipping_address = order.shipping_address
    if shipping_address is None:
        return redirect('orders:address')

    context = {
        'cart': cart,
        'breadcrumb': breadcrumb(address=True, confirmation=True),
        'order': order,
        'shipping_address': shipping_address,
    }

    return render(request, 'orders/confirm.html', context)


@login_required(login_url='login')
def cancel(request):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)

    if request.user.id != order.user_id:
        return redirect('carts:cart')

    order.cancel()

    messages.error(request,'Order canceled')
    destroy_cart(request)
    destroy_order(request)

    return redirect('index')

