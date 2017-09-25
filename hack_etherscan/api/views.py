# api/views.py

from rest_framework import generics
from .serializers import TopTokenHolderSerializer,TopTokenTransactionsSerializer
from polls.models import TopTokenHolder,TopTokenTransaction,Account,Token,ETHTransactoin,EtherBlock
from .models import *
from polls.views import get_all_transaction_data_for_a_token
from dateutil import parser
from django.http import JsonResponse,HttpResponse
import requests
from polls.tasks import get_ether_delta_inout_for_zrx

class RetriveTopTokenHolderView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = TopTokenHolder.objects.all()
    serializer_class = TopTokenHolderSerializer
    lookup_url_kwarg_time = "time"
    lookup_url_kwarg_token = "token"

    def get_queryset(self):
        timestamp_s = self.kwargs.get(self.lookup_url_kwarg_time)
        timestamp = parser.parse(timestamp_s)
        token_contract_address = self.kwargs.get(self.lookup_url_kwarg_token)
        token_obj = Token.objects.get(contract_address=token_contract_address)
        holders = TopTokenHolder.objects.filter(timestsamp=timestamp,token_name=token_obj)
        return holders

class RetriveTopTokenTransactionView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = TopTokenTransaction.objects.all()
    serializer_class = TopTokenTransactionsSerializer
    lookup_url_kwarg_time = "time"
    lookup_url_kwarg_token = "token"

    def get_queryset(self):
        timestamp_s = self.kwargs.get(self.lookup_url_kwarg_time)
        timestamp = parser.parse(timestamp_s)
        token_contract_address = self.kwargs.get(self.lookup_url_kwarg_token)
        token_obj = Token.objects.get(contract_address=token_contract_address)
        transactions = TopTokenTransaction.objects.filter(timestsamp=timestamp,token_name=token_obj)
        return transactions
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_account(request,account):
    memo = request.POST.get("memo",None)
    if memo is None:
        response = JsonResponse({'status':'false'}, status=400)
        return response
    account_obj = Account.objects.get(account_address=account)
    account_obj.gussed_name = memo
    account_obj.save()
    return JsonResponse({"status":"okay"})

from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
def add_token(request,token,token_name):
    if token is None or token == "":
        return JsonResponse({'status':'false','reason':'token not specified'},status=400)
    if token_name is None or token_name == "":
        return JsonResponse({'status': 'false', 'reason': 'token_name wrong'}, status=400)
    etherscan_api_url = "https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress={}&apikey=B4IFQIJ88Z36UYYRUHVRPTZ46HZ2S3FCCV".format(token)
    r = requests.get(etherscan_api_url)
    json_result = r.json()
    if json_result['result'] == "0":
        return JsonResponse({'status': 'false','reason':'token not found on etherscan'}, status=400)

    error = False
    try:
        dummy = Token.objects.get(contract_address=token)
        error = True
    except ObjectDoesNotExist:
        token_obj = Token(coin_name=token_name,contract_address=token)
        token_obj.status = "fetching_all_data"
        token_obj.save()
        get_all_transaction_data_for_a_token(token_name,token)

    if error:
        return JsonResponse({"status": "false", 'reason': 'token already exists'})
    else:
        return JsonResponse({"status": "okay"})
def get_all_tokens(request):
    tokens = Token.objects.all()
    results = []
    for token in tokens:
        results.append({"coin_name":token.coin_name,"contract_address":token.contract_address})
    return JsonResponse({'results': results})

from web3 import Web3, HTTPProvider, IPCProvider
web3 = Web3(HTTPProvider('http://localhost:8545'))
from django.db.models import Max

def get_etherdelta_input_for_zerox(request):
    blocks = EtherBlock.objects.all()
    max_block = blocks.aggregate(Max('block_number'))
    first_block = int(max_block["block_number__max"])
    last_block = web3.eth.blockNumber
    for block_number in range(first_block,last_block+1):
        print(block_number)
        get_ether_delta_inout_for_zrx.apply_async([block_number])
    return JsonResponse({"status": "okay"})
import re
split_re = re.compile(r'.{1,64}')
kyber_contarct_address = "dd974d5c2e2928dea5f71b9825b8b646686bd200"
etherdelta_trade_address = "0x0a19b14a"
eth_token_address = "0000000000000000000000000000000000000000000000000000000000000000"
wei = 1000000000000000000

from datetime import datetime
import time

def get_kyber_stat_on_etherdelta(request,timestamp):
    timestamp = parser.parse(timestamp)
    timestamp = timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
    kyber_etherdelta_txs = ETHTransactoin.objects.filter(input__contains=kyber_contarct_address).filter(input__contains=etherdelta_trade_address).filter(block_number__timestamp__year=timestamp.year,block_number__timestamp__month=timestamp.month,block_number__timestamp__day=timestamp.day)
    kyber_token = Token.objects.get(contract_address="0xdd974d5c2e2928dea5f71b9825b8b646686bd200")

    total_number_of_eth_buy = 0.0
    total_number_of_eth_sell = 0.0
    total_number_of_kyber_buy = 0.0
    total_number_of_kyber_sell = 0.0

    decoded_objs = []
    for tx in kyber_etherdelta_txs:
        input = tx.input[10:]
        assert(len(input)%64==0)
        input_arrs = split_re.findall(input)
        is_buyer = kyber_contarct_address in input_arrs[0]
        user_account = tx.from_account
        if is_buyer:
            price = int(input_arrs[3], 16) / int(input_arrs[1], 16)
            kyber_amount = int(input_arrs[1],16) / wei
            eth_amount = kyber_amount * price
            total_number_of_eth_buy += eth_amount
            total_number_of_kyber_buy += kyber_amount
            #print("buyer {}: {} {} ETH".format(tx.tx_hash.tx_hash,price,eth_amount))
        else:
            price = int(input_arrs[1],16) / int(input_arrs[3],16)
            kyber_amount = int(input_arrs[3],16) / wei
            eth_amount = kyber_amount * price
            total_number_of_eth_sell += eth_amount
            total_number_of_kyber_sell += kyber_amount
            #print("seller {}: {} {} ETH".format(tx.tx_hash.tx_hash,price,eth_amount))
        tx_hash = tx.tx_hash
        decoded_objs.append([is_buyer,user_account,price,kyber_amount,tx_hash,eth_amount])

    total_number_of_eth = total_number_of_eth_buy + total_number_of_eth_sell
    total_number_of_kyber = total_number_of_kyber_buy + total_number_of_kyber_sell

    try:
        old_stat = EtherDeltaDailyStat.objects.get(timestamp=timestamp,token_name=kyber_token)
        old_stat.delete()
    except:
        pass

    stat = EtherDeltaDailyStat(timestamp=timestamp,total_eth_buy=total_number_of_eth_buy,total_eth_sell=total_number_of_eth_sell,total_kyber_buy=total_number_of_kyber_buy,total_kyber_sell=total_number_of_kyber_sell,token_name=kyber_token,avg_price=(total_number_of_eth/total_number_of_kyber))
    stat.save()

    try:
        old_top_etherdelta_txs = TopEtherDeltaTransaction.objects.filter(token_name=kyber_token,timestamp=timestamp)
        old_top_etherdelta_txs.delete()
    except:
        pass

    sorted_decoded_objs = sorted(decoded_objs, key=lambda x: x[3], reverse=True)[:50]
    for obj in sorted_decoded_objs:
        is_buyer, user_account, price, kyber_amount, tx_hash, eth_amount = obj
        try:
            from_account = Account.objects.get(account_address=user_account)
        except:
            from_account = Account(account_address=user_account,gussed_name="")
            from_account.save()

        top_tx = TopEtherDeltaTransaction(token_name=kyber_token,tx_hash=tx_hash,timestamp=timestamp,from_account=from_account,eth_quantity=eth_amount,token_quantity=kyber_amount,price=price,is_buyer=is_buyer)
        top_tx.save()

    # m_top_etherDelta_transaction = TopEtherDeltaTransaction(token_name=kyber_token,tx_hash=tx_hash,timestamp=timestamp,from_account=user_account,)
    return JsonResponse({"status": "ok","number":str(len(kyber_etherdelta_txs))})
