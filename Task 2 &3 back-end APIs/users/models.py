from django.db import models
from GreenUser.models import GreenUser
from SubscriptionPlan.models import SubscriptionPlan


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=15, unique=True)
    username = models.CharField(max_length=50, unique=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    green_user_status = models.ForeignKey(GreenUser, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username
