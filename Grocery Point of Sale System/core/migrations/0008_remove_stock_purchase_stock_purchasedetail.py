# Generated by Django 4.2.1 on 2023-05-28 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_purchase_totalprice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='purchase',
        ),
        migrations.AddField(
            model_name='stock',
            name='purchasedetail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.purchasedetail'),
        ),
    ]
