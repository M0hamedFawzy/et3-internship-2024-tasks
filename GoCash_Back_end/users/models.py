from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from SubscriptionPlan.models import SubscriptionPlan
from GreenPlan.models import GreenPlan


class UserManager(BaseUserManager):
    def create_user(self, phone_number, username, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The Phone Number must be set')
        user = self.model(phone_number=phone_number, username=username, **extra_fields)
        if password:
            user.set_password(password)  # Hash the password
        else:
            user.set_unusable_password()  # Set an unusable password if none provided
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=15, unique=True)
    username = models.CharField(max_length=50)
    registration_date = models.DateTimeField(auto_now_add=True)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    green_user_status = models.ForeignKey(GreenPlan, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


