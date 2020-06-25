from django.db import models
from users.models import User


class ShippingAdress(models.Model):
    user = models.ForeignKey(User,
                             blank=False,
                             null=False,
                             on_delete=models.CASCADE)
    line1 = models.CharField(max_length=200)
    line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    reference = models.CharField(max_length=300)
    postal_code = models.CharField(max_length=10, blank=False, null=False)
    default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.postal_code

    @property
    def address(self):
        return '{} - {} - {}'.format(self.line1, self.city, self.country)

    def update_default(self, default=False):
        self.default = default
        self.save()

    def has_arders(self):
        return self.order_set.count() >= 1
