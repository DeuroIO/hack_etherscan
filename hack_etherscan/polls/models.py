# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Token(models.Model):
    def __str__(self):
        return self.coin_name + " " + self.contract_address
    coin_name = models.CharField(max_length=1024)
    contract_address = models.CharField(max_length=1024,unique=True)
    status = models.CharField(max_length=100)

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
    def __str__(self):
        return str(self.rank) + " " + self.token_name.coin_name + " " + self.account.account_address + " : " + str(self.top_amount) + " at " + self.timestsamp.strftime("%Y-%m-%d")
    token_name = models.ForeignKey(Token)
    timestsamp = models.DateTimeField()
    account = models.ForeignKey(Account,null=True)
    top_amount = models.FloatField(default=0.0)
    rank = models.IntegerField(default=0)

class TopTokenTransaction(models.Model):
    def __str__(self):
        return str(self.rank) + " " + self.token_name.coin_name + " : " + str(self.transaction.quantity) + " at " + self.timestsamp.strftime("%Y-%m-%d")
    token_name = models.ForeignKey(Token)
    timestsamp = models.DateTimeField()
    transaction = models.ForeignKey(TokenTransaction,null=True)
    rank = models.IntegerField(default=0)

class EtherTransactionHash(models.Model):
    def __str__(self):
        return self.tx_hash
    tx_hash = models.CharField(max_length=1024,unique=True)

# class EtherDeltaTokenTrade(models.Model):
#     def __str__(self):
#         is_buy = "buy" if self.is_buy else "sell"
#         return self.token_name.coin_name + " " + is_buy
#     token_name = models.ForeignKey(Token)
#     tx_hash = models.ForeignKey(EtherTransactionHash)
#     timestamp = models.DateTimeField()
#     price = models.FloatField()
#     is_buy = models.BooleanField()
#     amount = models.FloatField()
#     amount_base = models.FloatField()
#     buyer = models.ForeignKey(Account,null=True, related_name='buyer_account')
#     seller = models.ForeignKey(Account,null=True, related_name='seller_account')

class EtherBlock(models.Model):
    def __str__(self):
        return str(self.block_number) + " " + self.timestamp.strftime("%Y-%m-%d")
    block_number = models.FloatField(unique=True)
    timestamp = models.DateTimeField()

class ETHTransactoin(models.Model):
    def __str__(self):
        return self.tx_hash.tx_hash
    tx_hash = models.ForeignKey(EtherTransactionHash)
    nounce = models.FloatField()
    block_number = models.ForeignKey(EtherBlock)
    from_account = models.ForeignKey(Account, null=True, related_name='ETHTransactoin_from_account')
    to_account = models.ForeignKey(Account, null=True, related_name='ETHTransactoin_to_account')
    value = models.FloatField()
    gasPrice = models.FloatField()
    gas = models.FloatField()
    input = models.TextField()
