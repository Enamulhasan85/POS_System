# Generated by Django 4.2.1 on 2023-07-01 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_refund_totalprice'),
    ]

    operations = [
        migrations.RenameField(
            model_name='refund',
            old_name='totalPrice',
            new_name='totalRefund',
        ),
        migrations.AddField(
            model_name='refund',
            name='dueRefund',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
