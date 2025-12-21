from django.db import models
from django.contrib.auth.models import User

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
    pickup_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.status}"
