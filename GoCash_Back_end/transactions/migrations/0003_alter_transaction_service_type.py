# Generated by Django 5.1.1 on 2024-12-13 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='service_type',
            field=models.CharField(choices=[('Deposit', 'deposit'), ('Withdrawal', 'withdrawal'), ('Transaction', 'transaction'), ('Bill Payment', 'bill payment'), ('Mobile Bills', 'mobile bills'), ('Merchant Payment', 'merchant payment'), ('Account Subscription', 'account subscription'), ('Green Subscription', 'green subscription')], max_length=50, null=True),
        ),
    ]
