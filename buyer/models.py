from django.db import models
from django.utils import timezone

from datetime import timedelta

import secrets


class Buyer(models.Model):
    uid = models.CharField(primary_key=True, max_length=10, default='xxxxxxxxxx')
    fullname = models.CharField(max_length=100, null=True, default=None)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=20, null=True, default=None)
    password = models.CharField(max_length=256)

    is_verified = models.BooleanField(default=False)

    verification_code = models.CharField(max_length=6, blank=True, null=True)
    code_expires_at = models.DateTimeField(blank=True, null=True)


    def generate_verification_code(self, expiry_minutes=5):
        code = ''.join(secrets.choice('0123456789') for _ in range(6))
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


    def __str__(self):
        return str(self.email)


class Payment(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey("seller.Product", on_delete=models.SET_NULL, null=True, blank=True)
    order_id = models.CharField(max_length=100, unique=True)
    payment_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=50, default='Online Payment')
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)


class History(models.Model):
    product = models.ForeignKey("seller.Product", on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey("seller.Seller", on_delete=models.SET_NULL, null=True)
    date_of_purchase = models.DateTimeField(default=timezone.now, verbose_name="date of purchase")
    owner = models.ForeignKey(Buyer, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.product.name


class RouteError(models.Model):
    eid = models.CharField(max_length=15, primary_key=True, default='xxxxx-xxxxx')
    title = models.CharField(max_length=122)
    message = models.TextField()
    route = models.CharField(max_length=122)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return str(self.eid)
