# Generated by Django 4.2.1 on 2023-05-28 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_remove_stock_purchase_stock_purchasedetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='purchase',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.purchase'),
        ),
    ]
