# Generated by Django 5.1.4 on 2025-01-31 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruiz_clinic', '0045_remove_patient_patient_money'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='sales_recorded',
            field=models.BooleanField(default=False),
        ),
    ]
