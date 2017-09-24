# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-24 23:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='etherdeltadailystat',
            old_name='total_buy',
            new_name='total_eth_buy',
        ),
        migrations.RenameField(
            model_name='etherdeltadailystat',
            old_name='total_sell',
            new_name='total_eth_sell',
        ),
        migrations.AddField(
            model_name='etherdeltadailystat',
            name='total_kyber_buy',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='etherdeltadailystat',
            name='total_kyber_sell',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]
