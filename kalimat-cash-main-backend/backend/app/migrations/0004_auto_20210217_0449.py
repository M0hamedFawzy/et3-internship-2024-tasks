# Generated by Django 3.1.6 on 2021-02-17 02:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0003_auto_20210217_0425'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='تحويل',
            options={'verbose_name_plural': 'تحويل'},
        ),
        migrations.AlterModelOptions(
            name='سحب',
            options={'verbose_name_plural': 'سحب'},
        ),
        migrations.AlterModelOptions(
            name='شحن',
            options={'verbose_name_plural': 'شحن'},
        ),
        migrations.AlterModelOptions(
            name='فرع',
            options={'verbose_name_plural': 'فروع'},
        ),
        migrations.AlterModelOptions(
            name='موظف',
            options={'verbose_name_plural': 'موظفين'},
        ),
        migrations.AlterField(
            model_name='شحن',
            name='لصالح',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]