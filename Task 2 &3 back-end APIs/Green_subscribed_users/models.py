from django.db import models
from users.models import User
from GreenUser.models import GreenUser


class Green_subscribed_users(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    g_type = models.ForeignKey(GreenUser, on_delete=models.CASCADE)
    subscription_start_date = models.DateTimeField()
    subscription_end_date = models.DateTimeField()


def __str__(self):
    return f'{self.user.username} is a {self.g_type.green_type}'
