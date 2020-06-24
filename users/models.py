from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom Model User"""
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def shipping_address(self):
        return self.shippingadress_set.filter(default=True).first()

    def has_shipping_address(self):
        return self.shipping_address is not None

class Customer(User):
    """Model for customer"""
    class Meta:
        proxy = True

    def get_products(self):
        return []

class Profile(models.Model):
    """Model for profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
