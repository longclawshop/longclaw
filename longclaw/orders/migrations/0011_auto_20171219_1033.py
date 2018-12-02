# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-12-19 10:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20171008_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'Submitted'), (2, 'Fulfilled'), (3, 'Cancelled'), (4, 'Refunded'), (5, 'Payment Failed')], default=1),
        ),
    ]