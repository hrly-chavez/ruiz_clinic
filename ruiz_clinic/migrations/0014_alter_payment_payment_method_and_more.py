# Generated by Django 5.1.4 on 2024-12-19 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruiz_clinic', '0013_alter_payment_payment_method_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(choices=[('Cash', 'Cash'), ('Debit Card', 'Debit Card'), ('Credit Card', 'Credit Card'), ('E Wallet', 'E Wallet'), ('Other', 'Other')], default='Cash', max_length=50),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_terms',
            field=models.CharField(choices=[('Installment', 'Installment'), ('Fully Paid', 'Fully Paid')], default='Fully Paid', max_length=20),
        ),
    ]
