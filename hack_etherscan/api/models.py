from django.db import models
from polls.models import Token,EtherTransactionHash,Account
# Create your models here.
class EtherDeltaDailyStat(models.Model):
    def __str__(self):
        return self.token_name.coin_name + " " + self.avg_price + " at " + self.timestamp
    timestamp = models.DateTimeField()
    total_buy = models.FloatField()
    total_sell = models.FloatField()
    token_name = models.ForeignKey(Token)
    avg_price = models.FloatField()

class TopEtherDeltaTransaction(models.Model):
    def __str__(self):
        return self.tx_hash.tx_hash
    token_name = models.ForeignKey(Token)
    tx_hash = models.ForeignKey(EtherTransactionHash)
    timestamp = models.DateTimeField()
    from_account = models.ForeignKey(Account, null=True, related_name='top_etherDelta_transaction_from_account')
    eth_quantity = models.FloatField()
    token_quantity = models.FloatField()
    price = models.FloatField()