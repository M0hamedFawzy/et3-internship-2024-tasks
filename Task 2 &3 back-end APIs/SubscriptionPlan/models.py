from django.db import models


class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('standard', 'Standard'),
        ('plus', 'Plus'),
        ('premium', 'Premium'),
    ]

    name = models.CharField(max_length=10, choices=PLAN_CHOICES, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.name.capitalize()} - EGP{self.price}/month'
