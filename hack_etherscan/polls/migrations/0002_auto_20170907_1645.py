# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-07 16:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_address',
            field=models.CharField(max_length=1024, unique=True),
        ),
        migrations.AlterField(
            model_name='token',
            name='contract_address',
            field=models.CharField(max_length=1024, unique=True),
        ),
        migrations.AlterField(
            model_name='tokentransaction',
            name='tx_hash',
            field=models.CharField(max_length=1024, unique=True),
        ),
    ]