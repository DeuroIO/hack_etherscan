# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Token(models.Model):
    coin_name = models.CharField(max_length=1024)
    contract_address = models.CharField(max_length=1024)

class Account(models.Model):
    gussed_name = models.CharField(max_length=1024)
    account_address = models.CharField(max_length=1024)

class TokenTransaction(models.Model):
    def __str__(self):
        return self.token_name + ": from " + self.from_account + " to " + self.to_account + " " + self.quantity
    token_name = models.ForeignKey(Token)
    tx_hash = models.CharField(max_length=1024)
    timestamp = models.DateTimeField()
    from_account = models.ForeignKey(Account,null=True, related_name='from_account')
    to_account = models.ForeignKey(Account,null=True, related_name='to_account')
    quantity = models.FloatField()
