# Generated by Django 5.1.4 on 2025-02-03 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruiz_clinic', '0050_alter_checkuphistory_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='patient_date_checked_up',
            field=models.DateField(blank=True, null=True),
        ),
    ]
