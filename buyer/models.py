from django.db import models
from django.utils import timezone

from seller.models import Product, Seller


class Buyer(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length=256)

    def __str__(self):
        return self.email


class History(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True)
    date_of_purchase = models.DateTimeField(default=timezone.now, verbose_name="date of purchase")
    owner = models.ForeignKey(Buyer, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.product.name


class RouteError(models.Model):
    title = models.CharField(max_length=122)
    message = models.TextField()
    field = models.CharField(max_length=122)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.title