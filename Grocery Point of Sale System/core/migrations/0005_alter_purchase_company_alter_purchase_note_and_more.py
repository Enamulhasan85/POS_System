# Generated by Django 4.2.1 on 2023-05-26 15:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_purchase_company_stock_purchase_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='core.company'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchase',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchasedetail',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.product'),
        ),
        migrations.AlterField(
            model_name='purchasedetail',
            name='purchase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.purchase'),
        ),
    ]
