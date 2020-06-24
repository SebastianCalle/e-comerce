from django.db import models

from enum import Enum

from users.models import User
from carts.models import Cart
from shipping_address.models import ShippingAdress

from django.db.models.signals import pre_save

import uuid
# Create your models here.

class OrderStatus(Enum):
    """Status of the order"""
    CREATED = 'CREATED'
    PAYED = 'PAYED'
    CANCELED = 'CANCELED'

choices = [(tag, tag.value) for tag in OrderStatus]

class Order(models.Model):
    """Model for Order"""
    order_id = models.CharField(max_length=100, null=False, blank=False,
                               unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(ShippingAdress,
                                         null=True, blank=True,
                                         on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=choices,
                              default=OrderStatus.CREATED)
    shipping_total = models.DecimalField(default=5, max_digits=8,
                                         decimal_places=2)
    total = models.DecimalField(default=5, max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id

    def update_total(self):
        self.total = self.get_total()
        self.save()

    def get_or_set_shipping_address(self):
        if self.shipping_address:
            return self.shipping_address

        shipping_address = self.user.shipping_address
        if shipping_address:
            self.shipping_address = shipping_address
            self.save()

        return shipping_address

    def get_total(self):
        return self.cart.total + self.shipping_total

def set_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = str(uuid.uuid4())

def set_total(sender, instance, *args, **kwargs):
    instance.total = instance.get_total()


pre_save.connect(set_order_id, sender=Order)
pre_save.connect(set_total, sender=Order)
