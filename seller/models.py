from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from pyotp import random_base32
from datetime import timedelta
from pyotp.totp import TOTP
from secrets import choice


class Seller(models.Model):
    uid = models.CharField(primary_key=True, max_length=10, default='xxxxxxxxxx')
    username = models.CharField(max_length=122, unique=True)
    fullname = models.CharField(max_length=122, null=True)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length=122)

    is_verified = models.BooleanField(default=False)

    verification_code = models.CharField(max_length=6, blank=True, null=True)
    code_expires_at = models.DateTimeField(blank=True, null=True)

    twoFA_secret = models.CharField(max_length=32, blank=True, null=True)
    qr_code_path = models.ImageField(upload_to='auth-QRs/', blank=True, null=True)

    def generate_verification_code(self, expiry_minutes=5):
        code = ''.join(choice('0123456789') for _ in range(6))
        self.verification_code = code
        self.code_expires_at = timezone.now() + timedelta(minutes=expiry_minutes)
        self.save()

        return code

    def validate_code(self, submitted_code):
        if not self.verification_code or not self.code_expires_at:return False, "No code generated"
        if self.verification_code != submitted_code: return False, "Invalid code"
        if timezone.now() > self.code_expires_at: return False, "Code expired"

        return True, "Code is valid"

    def clear_verification_code(self):
        self.verification_code = None
        self.code_expires_at = None
        self.save()

    def get_otp_uri(self):
        if not self.twoFA_secret:
            self.twoFA_secret = random_base32()
            self.save()

        return TOTP(str(self.twoFA_secret)).provisioning_uri(
            name=str(self.email),
            issuer_name="P.O.Bucket"
        )

    def verify2FAcode(self, code):
        totp = TOTP(str(self.twoFA_secret))
        if totp.verify(code): return True

        try:
            backup_codes = BackupCodes.objects.get(seller=self)
            if backup_codes and code in backup_codes.codes:
                backup_codes.codes.remove(code)
                backup_codes.save()
                return True
            return False

        except ObjectDoesNotExist: pass
        return False

    def __str__(self) -> str:
        return str(self.username)


class BackupCodes(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='backup_codes')
    codes = models.JSONField(default=list, blank=True)

    def __str__(self):
        return str(self.seller)


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
    image = models.ImageField(upload_to='products/', blank=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='product')
    publish_date = models.DateTimeField(default=timezone.now, verbose_name="publish date")
    bid_status = models.BooleanField(default=False, verbose_name="bit status")  # Flag to mark if auction/bidding is open
    highest_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Highest bid amount
    highest_bidder = models.ForeignKey("buyer.Buyer", null=True, blank=True, on_delete=models.SET_NULL, related_name="bids_won")

    def __str__(self) -> str:
        return str(self.name)


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


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name="sale")  # Product sold
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="sale")  # Seller
    buyer = models.ForeignKey("buyer.Buyer", on_delete=models.SET_NULL, null=True, blank=True, related_name="purchases")  # Buyer
    payment = models.ForeignKey("buyer.Payment", on_delete=models.SET_NULL, null=True, blank=True, related_name="sale")  # Payment
    final_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Sale price (highest bid or base price)
    sale_date = models.DateTimeField(default=timezone.now, verbose_name="Sale Date")  # Date of sale

    def __str__(self):
        return self.product.name


class RouteError(models.Model):
    eid = models.CharField(max_length=15, primary_key=True, default='xxxxx-xxxxx')
    title = models.CharField(max_length=122)
    message = models.TextField()
    route = models.CharField(max_length=122)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return str(self.eid)
