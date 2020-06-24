from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import ShippingAdress
from .forms import ShippingAdressForm
from users.models import User


# Create your views here.
class ShippingAddressListView(LoginRequiredMixin, ListView):
    """View for shipping address"""
    login_url = 'login'
    model = ShippingAdress
    template_name = 'shipping_address/shipping_addresses.html'

    def get_queryset(self):
        return ShippingAdress.objects.filter(user=self.request.user).order_by('-default')

class ShippingAddressUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """View for update shipping address"""
    login_url = 'login'
    model = ShippingAdress
    form_class = ShippingAdressForm
    template_name = 'shipping_address/update.html'
    success_message = 'Direction update successfully'

    def get_success_url(self):
        return reverse('shipping_address:shipping_address')

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().user_id:
            return redirect('carts:cart')

        return super(ShippingAddressUpdateView, self).dispatch(request, *args, **kwargs)

class ShippingAdressDeleteView(LoginRequiredMixin, DeleteView):
    login_url = 'login'
    model = ShippingAdress
    template_name = 'shipping_address/delete.html'
    success_message = 'Direction deleted successfully'
    success_url = reverse_lazy('shipping_address:shipping_address')

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().default:
            return redirect('shipping_address:shipping_address')

        if request.user.id != self.get_object().user_id:
            return redirect('carts:cart')

        return super(ShippingAdressDeleteView, self).dispatch(request, *args, **kwargs)

@login_required(login_url='login')
def create(request):
    form = ShippingAdressForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        shipping_address = form.save(commit=False)
        shipping_address.user = request.user
        shipping_address.default = not ShippingAdress.objects.filter(user=request.user).exists()

        shipping_address.save()

        messages.success(request, 'Direction created succesful')
        return redirect('shipping_address:shipping_address')

    context = { 'form': form }
    return render(request, 'shipping_address/create.html', context)

@login_required(login_url='login')
def default(request, pk):
    address = get_object_or_404(ShippingAdress, pk=pk)

    if request.user.id != address.user_id:
        return redirect('carts:cart')

    if request.user.has_shipping_address():
        request.user.shipping_address.update_default()

    address.update_default(True)

    return redirect('shipping_address:shipping_address')

