from django.db import models
from users.models import User
from SubscriptionPlan.models import SubscriptionPlan


class Plan_subscribed_users(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    subscription_start_date = models.DateTimeField()
    subscription_end_date = models.DateTimeField()


def __str__(self):
    return f'{self.user.username} with Plan {self.plan.name}'
