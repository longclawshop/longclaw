# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-13 08:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_order_transaction_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]