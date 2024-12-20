# Generated by Django 4.2.1 on 2023-06-20 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_supplier_remove_purchase_provider_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchasedetail',
            name='unit',
        ),
        migrations.RemoveField(
            model_name='saledetail',
            name='unit',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='unit',
        ),
        migrations.AddField(
            model_name='product',
            name='unit',
            field=models.CharField(choices=[('kg', 'KG'), ('litre', 'Litre'), ('piece', 'Piece'), ('feet', 'Feet')], default=1, max_length=20),
            preserve_default=False,
        ),
    ]
