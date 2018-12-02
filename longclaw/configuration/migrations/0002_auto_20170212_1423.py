# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-12 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='default_shipping_carrier',
            field=models.CharField(default='Royal Mail', help_text='The default shipping carrier', max_length=32),
        ),
        migrations.AlterField(
            model_name='settings',
            name='default_shipping_rate',
            field=models.DecimalField(decimal_places=2, default=3.95, help_text='The default shipping rate for countries which have not been configured', max_digits=12),
        ),
    ]