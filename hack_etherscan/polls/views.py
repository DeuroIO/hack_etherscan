# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse

# Create your views here.
from .html_helper import get_html_by_url
from .models import Token
from .tasks import get_tokens_from_view_a_tokentxns_page

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