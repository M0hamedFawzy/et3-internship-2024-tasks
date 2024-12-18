from django.db import models


class GreenUser(models.Model):
    GREEN_CHOICES = [
        ('leaf', 'Leaf'),
        ('tree', 'Tree'),
        ('forest', 'Forest'),
    ]

    green_type = models.CharField(max_length=6, choices=GREEN_CHOICES, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.green_type.capitalize()} - EGP{self.price}/month'
