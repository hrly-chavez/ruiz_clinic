# Generated by Django 5.1.4 on 2024-12-29 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruiz_clinic', '0020_merge_20241229_2221'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
