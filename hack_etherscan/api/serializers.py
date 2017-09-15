from rest_framework import serializers
from polls.models import TokenTransaction,Account,Token


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = ('coin_name', 'contract_address')

class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('gussed_name', 'account_address')

class TokenTransactionSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    token_name = TokenSerializer()
    from_account = AccountSerializer()
    to_account = AccountSerializer()

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = TokenTransaction
        fields = ('token_name', 'tx_hash', 'timestamp','from_account','to_account','quantity')