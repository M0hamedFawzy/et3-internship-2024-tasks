from django.db import models


class DimDate(models.Model):
    date_id = models.AutoField(primary_key=True)
    date = models.DateField()
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()
    quarter = models.IntegerField()
    weekday = models.CharField(max_length=10)

    class Meta:
        app_label = 'dwbi'
        db_table = 'dimdate'
        managed = False  # Since this data is maintained in the external database


class DimUser(models.Model):
    user_id = models.IntegerField(primary_key=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    username = models.CharField(max_length=50, null=True, blank=True)
    registration_date = models.DateField(null=True, blank=True)
    subscription_plan_id = models.IntegerField(null=True, blank=True)
    green_user_status_id = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    class Meta:
        app_label = 'dwbi'
        db_table = 'dimuser'
        managed = False


class DimServiceType(models.Model):
    service_type_id = models.AutoField(primary_key=True)
    service_type = models.CharField(max_length=50)
    service_name = models.CharField(max_length=50)

    class Meta:
        app_label = 'dwbi'
        db_table = 'dimservicetype'
        managed = False


class DimWallet(models.Model):
    wallet_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(DimUser, on_delete=models.CASCADE, db_column='user_id')
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        app_label = 'dwbi'
        db_table = 'dimwallet'
        managed = False


class FactTransaction(models.Model):
    transaction_id = models.IntegerField(primary_key=True)  # No auto-increment
    date = models.ForeignKey(DimDate, on_delete=models.CASCADE, db_column='date_id')
    user = models.ForeignKey(DimUser, on_delete=models.CASCADE, db_column='user_id')
    wallet = models.ForeignKey(DimWallet, on_delete=models.CASCADE, db_column='wallet_id')
    service_type = models.ForeignKey(DimServiceType, on_delete=models.CASCADE, db_column='service_type_id')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    balance_before = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField()

    class Meta:
        app_label = 'dwbi'
        db_table = 'facttransaction'
        managed = False
        unique_together = ('transaction_id', 'date')  # Mimic composite key constraint


