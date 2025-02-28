# Generated by Django 5.1.4 on 2025-01-21 06:10

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruiz_clinic', '0041_alter_purchased_item_pur_stat'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment_Duration',
            fields=[
                ('payment_duration_id', models.AutoField(primary_key=True, serialize=False)),
                ('payment_duration_span', models.CharField(choices=[('3 Months', '3 Months'), ('6 Months', '6 Months'), ('9 Months', '9 Months'), ('12 Months', '12 Months')], max_length=50)),
                ('payment_duration_start', models.DateField(default=django.utils.timezone.now)),
                ('payment_duration_end', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_duration',
            field=models.ForeignKey(blank=True, help_text="Applicable only if payment terms are 'Installment'.", null=True, on_delete=django.db.models.deletion.SET_NULL, to='ruiz_clinic.payment_duration'),
        ),
    ]
