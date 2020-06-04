from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('users/login/', views.login_view, name='login'),
    path('users/logout/', views.logout_view, name='logout'),
    path('users/register/', views.register_view, name='register'),
]
