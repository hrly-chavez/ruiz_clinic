# Generated by Django 5.1.4 on 2024-12-31 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruiz_clinic', '0020_merge_20241231_1051'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('account_id', models.AutoField(primary_key=True, serialize=False)),
                ('account_username', models.CharField(max_length=50)),
                ('account_password', models.CharField(max_length=50)),
            ],
        ),
    ]
