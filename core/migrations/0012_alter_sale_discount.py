# Generated by Django 4.2.1 on 2023-06-20 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_remove_purchasedetail_unit_remove_saledetail_unit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='discount',
            field=models.FloatField(default=0),
        ),
    ]