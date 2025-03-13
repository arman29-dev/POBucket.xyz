from django.db import models
from django.utils import timezone


class Seller(models.Model):
    username = models.CharField(max_length=122, unique=True)
    fullname = models.CharField(max_length=122)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=122)

    def __str__(self) -> str:
        return self.username


class Product(models.Model):
    categories = [
        ('software', "Software"),
        ('hardware', "Hardware"),
        ('EEMS', "Electronics (embedded systems)")
    ]

    pid = models.CharField(max_length=122, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    desc = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=10, choices=categories, default='software')
    tags = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to=f'products/', blank=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='product')
    publish_date = models.DateTimeField(default=timezone.now, verbose_name="publish date")
    bid_status = models.BooleanField(default=False, verbose_name="bit status")  # Flag to mark if auction/bidding is open
    highest_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Highest bid amount
    highest_bidder = models.ForeignKey("buyer.Buyer", null=True, blank=True, on_delete=models.SET_NULL, related_name="bids_won")

    def __str__(self) -> str:
        return self.name


class Bid(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='bids')  # Product being bid on
    bidder = models.ForeignKey("buyer.Buyer", on_delete=models.CASCADE, related_name='bids')  # Buyer placing the bid
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Bid Amount")
    bid_time = models.DateTimeField(default=timezone.now, verbose_name="Bid Time")

    class Meta:
        ordering = ["-bid_amount"]  # Show highest bids first

    def __str__(self):
        return f"{self.bidder.username} bid ₹{self.bid_amount} on {self.product.name}"

    # Save and update product's highest bid
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update highest bid on product
        highest_bid = self.product.bids.order_by('-bid_amount').first()
        if highest_bid:
            self.product.highest_bid = highest_bid.bid_amount
            self.product.highest_bidder = highest_bid.bidder
            self.product.save()


class Sales(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="sales")  # Product sold
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="sales")  # Seller
    buyer = models.ForeignKey("buyer.Buyer", on_delete=models.CASCADE, null=True, blank=True, related_name="purchases")  # Buyer
    final_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Sale price (highest bid or base price)
    sale_date = models.DateTimeField(default=timezone.now, verbose_name="Sale Date")  # Date of sale

    def __str__(self):
        return f"{self.product.name} sold by {self.seller.username} to {self.buyer.username} for ₹{self.final_price}"


class RouteError(models.Model):
    title = models.CharField(max_length=122)
    message = models.TextField()
    field = models.CharField(max_length=122)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.title