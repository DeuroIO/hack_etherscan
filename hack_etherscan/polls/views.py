# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
import datetime
# Create your views here.
from .html_helper import get_html_by_url
from .models import Token,TokenTransaction
from .tasks import get_tokens_from_view_a_tokentxns_page,get_token_tx_from_a_page,calculate_today_top_stat

#get all tokens from https://etherscan.io/tokens
def get_tokens_from_view_tokens_page(request):
    base_url = "https://etherscan.io/tokens"
    soup = get_html_by_url(base_url)
    h5s = soup.find_all("h5")
    tokens = dict()
    for h5 in h5s:
        token_name = h5.text

        #get token_contract address
        half_url = h5.find("a")["href"]
        whole_url = "https://etherscan.io{}".format(half_url)
        token_soup = get_html_by_url(whole_url)
        contract_tr = token_soup.find("tr",{"id":"ContentPlaceHolder1_trContract"})
        contract_td = contract_tr.find_all('td')[1]
        contract_address = contract_td.text

        tokens[contract_address] = token_name
        print(whole_url)


    for contract_address in tokens:
        token_name = tokens[contract_address]
        t = Token(coin_name=token_name,contract_address=contract_address)
        print(t)
        t.save()

    return HttpResponse("succesfully get_tokens_from_view_tokens_page")

def get_tokens_from_view_tokentxns_page(request):
    base_url = "https://etherscan.io/tokentxns"

    for x in range(1,20001):
        tmp_url = "{}?p={}".format(base_url,x)
        print(tmp_url)
        get_tokens_from_view_a_tokentxns_page.delay(tmp_url)

    return HttpResponse("succesfully get_tokens_from_view_tokens_page")


from .crawl import get_transcripts_at_p,get_html_by_url

def get_total_number_of_pages_for_a_token(contract_address):
    soup = get_html_by_url("https://etherscan.io/token/generic-tokentxns2?contractAddress={}".format(contract_address))
    span_style = soup.find("span",{"style":"padding: 2px 4px 4px 3px; border: 1px solid #D4D4D4; line-height: 30px; background-color: #EAEAEA; margin-top: 2px; height: 2px;"})
    second_b = span_style.findAll("b")[1].text
    return int(second_b)

zero_x_contract_address = "0xe41d2489571d322189246dafa5ebde1f4699f498"
kyber_contract_address = "0xdd974d5c2e2928dea5f71b9825b8b646686bd200"

import threading
def get_kyber_network_crowd_sale_data():

    first_page = 1

    #check_the_last_page
    #last_page = get_total_number_of_pages_for_a_token(kyber_contract_address) + 1
    before_start_time = datetime.datetime.now()
    last_page = 2 
    for x in range(first_page,last_page+1):
        get_token_tx_from_a_page.delay("kyber",kyber_contract_address,x)
    print("get_0x_network_crowd_sale_data {}: {}".format(last_page,datetime.datetime.now()-before_start_time))

    threading.Timer(0.5, get_kyber_network_crowd_sale_data).start() # called every minute

def calculate_kyber_top_stat():
    calculate_today_top_stat.delay(kyber_contract_address)
    threading.Timer(60.0, calculate_kyber_top_stat).start()

get_kyber_network_crowd_sale_data()
calculate_today_top_stat(kyber_contract_address)