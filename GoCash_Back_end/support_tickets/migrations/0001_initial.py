# Generated by Django 5.1.1 on 2024-09-28 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SupportTicket',
            fields=[
                ('ticket_id', models.AutoField(primary_key=True, serialize=False)),
                ('issue_description', models.TextField(max_length=1000)),
                ('status', models.CharField(choices=[('open', 'Open'), ('closed', 'Closed'), ('in_progress', 'In Progress')], default='open', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
