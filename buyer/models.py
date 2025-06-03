from django.db import models
from django.utils import timezone

from datetime import timedelta

import secrets


class Buyer(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=20, null=True, default=None)
    password = models.CharField(max_length=256)

    verification_code = models.CharField(max_length=6, blank=True, null=True)
    code_expires_at = models.DateTimeField(blank=True, null=True)


    def generate_2FA_code(self, expiry_minutes=5):
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


class History(models.Model):
    product = models.ForeignKey("seller.Product", on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey("seller.Seller", on_delete=models.SET_NULL, null=True)
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
        return str(self.title)
