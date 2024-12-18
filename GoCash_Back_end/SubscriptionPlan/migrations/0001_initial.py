# Generated by Django 5.1.1 on 2024-09-28 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('standard', 'Standard'), ('plus', 'Plus'), ('premium', 'Premium')], max_length=10, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
    ]
