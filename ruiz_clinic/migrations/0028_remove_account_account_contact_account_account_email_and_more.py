# Generated by Django 5.1.4 on 2025-01-18 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruiz_clinic', '0027_merge_20250118_1014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='account_contact',
        ),
        migrations.AddField(
            model_name='account',
            name='account_email',
            field=models.CharField(default=1, max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account',
            name='account_username',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
