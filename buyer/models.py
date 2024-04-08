from django.db import models
from django.utils import timezone



class Buyer(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=122)

    def __str__(self):
        return self.email


class History(models.Model):
    product_name = models.CharField(max_length=122, verbose_name="product name")
    seller_phone_no = models.CharField(max_length=20, null=True, verbose_name="seller phone number")
    date_of_purchase = models.DateTimeField(default=timezone.now, verbose_name="date of purchase")
    owner = models.ForeignKey(Buyer, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.product_name


class RouteError(models.Model):
    title = models.CharField(max_length=122)
    message = models.TextField()
    field = models.CharField(max_length=122)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.title