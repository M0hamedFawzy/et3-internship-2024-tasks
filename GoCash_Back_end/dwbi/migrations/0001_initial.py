# Generated by Django 5.1.1 on 2024-12-03 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DimDate',
            fields=[
                ('date_id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('day', models.IntegerField()),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
                ('quarter', models.IntegerField()),
                ('weekday', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'dimdate',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DimServiceType',
            fields=[
                ('service_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('service_type', models.CharField(max_length=50)),
                ('service_name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'dimservicetype',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DimUser',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('username', models.CharField(blank=True, max_length=50, null=True)),
                ('registration_date', models.DateField(blank=True, null=True)),
                ('subscription_plan_id', models.IntegerField(blank=True, null=True)),
                ('green_user_status_id', models.IntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'dimuser',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DimWallet',
            fields=[
                ('wallet_id', models.IntegerField(primary_key=True, serialize=False)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'dimwallet',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FactTransaction',
            fields=[
                ('transaction_id', models.IntegerField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fees', models.DecimalField(decimal_places=2, max_digits=10)),
                ('balance_before', models.DecimalField(decimal_places=2, max_digits=10)),
                ('balance_after', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'facttransaction',
                'managed': False,
            },
        ),
    ]