# Generated by Django 4.2.1 on 2023-06-21 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_alter_sale_customer_alter_sale_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saledetail',
            name='refund',
        ),
        migrations.AddField(
            model_name='saledetail',
            name='discount',
            field=models.FloatField(default=0),
        ),
    ]
