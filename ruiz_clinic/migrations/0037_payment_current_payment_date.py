# Generated by Django 5.1.4 on 2025-01-20 11:41

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruiz_clinic', '0036_payment_current_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='current_payment_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
