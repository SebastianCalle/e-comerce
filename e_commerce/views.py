from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth.models import User


def index(request):
    """Index page"""
    return render(request, 'index.html', {})


def login_view(request):
    """Login page"""
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome {user.username}')
            return redirect('index')
        else:
            messages.error(request, 'User or password incorrect')

    return render(request, 'users/login.html', {})


def logout_view(request):
    """Logout page"""
    logout(request)
    messages.success(request, 'Logout succes')
    return redirect('login')


def register_view(request):
    """Register page"""
    if request.user.is_authenticated:
        return redirect('index')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        user = form.save()
        if user:
            login(request, user)
            print('creo user')
            messages.success(request, 'User create successfully')
            return redirect('index')


    context = {'form': form}
    return render(request, 'users/register.html', context)
