# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-08 14:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('longclaworders', '0009_auto_20170526_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'Submitted'), (2, 'Fulfilled'), (3, 'Cancelled'), (4, 'Refunded')], default=1),
        ),
    ]