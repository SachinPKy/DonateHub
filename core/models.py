from django.db import models
from django.contrib.auth.models import User
import random


class Donation(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Picked Up', 'Picked Up'),
        ('Delivered', 'Delivered'),
        ('Rejected', 'Rejected'),
    ]

    donor = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    description = models.TextField()

    # 🔹 ADD LOCATION HERE
    location = models.CharField(max_length=255)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    pickup_date = models.DateField()

    # 🔹 ADD PHOTO HERE
    photo = models.ImageField(
        upload_to="donations/",
        null=True,
        blank=True
    )

    receipt_generated_at = models.DateTimeField(
        null=True,
        blank=True
    )

    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_verified = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def generate_otp(self):
        if not self.otp:
            self.otp = str(random.randint(100000, 999999))

    def __str__(self):
        return f"{self.category} - {self.status}"
