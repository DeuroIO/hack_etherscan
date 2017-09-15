# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Token(models.Model):
    def __str__(self):
        return self.coin_name + " " + self.contract_address
    coin_name = models.CharField(max_length=1024)
    contract_address = models.CharField(max_length=1024,unique=True)

class Account(models.Model):
    def __str__(self):
        return  self.gussed_name + " " + self.account_address
    gussed_name = models.CharField(max_length=1024)
    account_address = models.CharField(max_length=1024,unique=True)

class TokenTransaction(models.Model):
    def __str__(self):
        return self.token_name.coin_name + ": from " + self.from_account.account_address + " to " + self.to_account.account_address + " " + str(self.quantity)
    token_name = models.ForeignKey(Token)
    tx_hash = models.CharField(max_length=1024,unique=True)
    timestamp = models.DateTimeField()
    from_account = models.ForeignKey(Account,null=True, related_name='from_account')
    to_account = models.ForeignKey(Account,null=True, related_name='to_account')
    quantity = models.FloatField()

class TopTokenHolder(models.Model):
    token_name = models.ForeignKey(Token)
    timestsamp = models.DateTimeField()
    account = models.ForeignKey(Account,null=True)
    top_amount = models.FloatField(default=0.0)
    rank = models.IntegerField(default=0)

class TopTokenTransaction(models.Model):
    token_name = models.ForeignKey(Token)
    timestsamp = models.DateTimeField()
    transaction = models.ForeignKey(TokenTransaction,null=True)
    rank = models.IntegerField(default=0)
