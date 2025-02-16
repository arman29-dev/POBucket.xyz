from django.db import models
from django.utils import timezone

from buyer.models import Buyer


class Seller(models.Model):
    username = models.CharField(max_length=122, unique=True)
    fullname = models.CharField(max_length=122)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=122)

    def __str__(self) -> str:
        return self.username


class Product(models.Model):
    categories = {
        0: "--SELECT CATEGORY--",
        1: "Software",
        2: "Hardware",
        3: "Electronics (embedded systems)",
    }

    pid = models.CharField(max_length=122, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    desc = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=5, choices=categories, default=0)
    tags = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to=f'products/', blank=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='product')
    publish_date = models.DateTimeField(default=timezone.now, verbose_name="publish date")
    bid_status = models.BooleanField(default=False, verbose_name="bit status")  # Flag to mark if auction/bidding is open

    def __str__(self) -> str:
        return self.pid


class Bid(models.Model):
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="bit amount")
    bid_time = models.DateTimeField(default=timezone.now, verbose_name="bit time")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Product of the Bid
    bidder = models.ForeignKey(Buyer, on_delete=models.CASCADE)  # User placing the bid

    class Meta:
        # Ensure only one highest bid exists per product
        ordering = ["-bid_amount"]

    def __str__(self) -> str:
        return self.product.pid


class Sales(models.Model):
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="sale price")
    date_of_sale = models.DateTimeField(default=timezone.now, verbose_name="date of sale")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.product.pid


class RouteError(models.Model):
    title = models.CharField(max_length=122)
    message = models.TextField()
    field = models.CharField(max_length=122)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.title