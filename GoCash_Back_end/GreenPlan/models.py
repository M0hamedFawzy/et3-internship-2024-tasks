from django.db import models
from datetime import timedelta


class GreenPlan(models.Model):
    GREEN_CHOICES = [
        ('leaf', 'Leaf'),
        ('tree', 'Tree'),
        ('forest', 'Forest'),
    ]

    green_type = models.CharField(max_length=6, choices=GREEN_CHOICES, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.green_type.capitalize()} - EGP{self.price}/month'


class GreenSubscribedUsers(models.Model):
    user_phone_number = models.CharField(max_length=15)
    g_type = models.ForeignKey(GreenPlan, on_delete=models.CASCADE)
    subscription_start_date = models.DateTimeField()
    subscription_end_date = models.DateTimeField()

    def __str__(self):
        return f'{self.user_phone_number} is a {self.g_type.green_type}'

    @classmethod
    def create_green_subscription_history(cls, user_p_n, g_plan, sub_start_date):
        """ Create User Subscription History"""
        sub_end_date = sub_start_date + timedelta(days=30)
        cls.objects.create(
            user_phone_number=user_p_n,
            g_type=g_plan,
            subscription_start_date=sub_start_date,
            subscription_end_date=sub_end_date
        )


