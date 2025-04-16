from django.db import models
from django.contrib.auth.models import User

FREQUENCY_CHOICES = [
    ('daily', 'daily'),
    ('weekly', 'weekly'),
    ('monthly', 'monthly'),
    ('yearly', 'yearly'),
]


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    next_billing_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.frequency})"
