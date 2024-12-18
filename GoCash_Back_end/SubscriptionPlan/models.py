from django.db import models
from datetime import timedelta


class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('Standard', 'Standard'),
        ('Plus', 'Plus'),
        ('Premium', 'Premium'),
    ]

    name = models.CharField(max_length=10, choices=PLAN_CHOICES, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    max_balance = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    max_transactions = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'{self.name.capitalize()} - EGP{self.price}/month'


class PlanSubscribedUsers(models.Model):
    user_phone_number = models.CharField(max_length=15)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    subscription_start_date = models.DateTimeField()
    subscription_end_date = models.DateTimeField()

    def __str__(self):
        return f'{self.user_phone_number} with Plan {self.plan.name}'

    @classmethod
    def create_subscription_history(cls, user_p_n, plan, sub_start_date):
        """ Create User Subscription History"""
        sub_end_date = sub_start_date + timedelta(days=30)
        cls.objects.create(
            user_phone_number=user_p_n,
            plan=plan,
            subscription_start_date=sub_start_date,
            subscription_end_date=sub_end_date
        )




