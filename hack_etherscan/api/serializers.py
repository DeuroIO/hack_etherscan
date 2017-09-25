from rest_framework import serializers
from polls.models import TokenTransaction,Account,Token,TopTokenHolder,TopTokenTransaction,EtherTransactionHash
from .models import *

class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = ('coin_name', 'contract_address')

class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('gussed_name', 'account_address')

class TransactionSerializer(serializers.ModelSerializer):
    from_account = AccountSerializer()
    to_account = AccountSerializer()

    class Meta:
        model = TokenTransaction
        fields = ('tx_hash', 'timestamp','from_account','to_account','quantity')

class TopTokenHolderSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    token_name = TokenSerializer()
    account = AccountSerializer()

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = TopTokenHolder
        fields = ('token_name', 'timestsamp', 'account','top_amount','rank')

class TopTokenTransactionsSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    token_name = TokenSerializer()
    transaction = TransactionSerializer()

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = TopTokenTransaction
        fields = ('token_name', 'timestsamp', 'transaction','rank')

class EtherTransactionHashSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtherTransactionHash
        fields=  ('tx_hash',)


class TopEtherDeltaTransactionsSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    token_name = TokenSerializer()
    from_account = AccountSerializer()
    tx_hash = EtherTransactionHashSerializer()

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = TopEtherDeltaTransaction
        fields = ('token_name', 'tx_hash', 'timestamp','from_account','eth_quantity','token_quantity','price','is_buyer')
    
    
class EtherDeltaDailyStatSerializer(serializers.ModelSerializer):
    token_name = TokenSerializer()

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = EtherDeltaDailyStat
        fields = (
        'token_name', 'timestamp', 'total_eth_buy', 'total_eth_sell', 'total_kyber_buy', 'total_kyber_sell', 'token_name', 'avg_price')
