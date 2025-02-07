# Generated by Django 5.1.4 on 2025-02-07 12:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruiz_clinic', '0046_payment_sales_recorded'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('doctor_id', models.AutoField(primary_key=True, serialize=False)),
                ('doctor_fname', models.CharField(max_length=50)),
                ('doctor_lname', models.CharField(max_length=50)),
                ('doctor_initial', models.CharField(max_length=1)),
                ('doctor_specialization', models.CharField(max_length=100)),
                ('doctor_contact', models.CharField(max_length=13)),
                ('doctor_address', models.CharField(max_length=400)),
                ('doctor_birthdate', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='doctor_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ruiz_clinic.doctor'),
        ),
    ]
