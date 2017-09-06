from bs4 import BeautifulSoup
import sys
from re import sub
from decimal import Decimal
import datetime
import re
import urllib2
from dateutil import parser
import sqlite3
from sqlite3 import Error

def get_html_by_url(url):
    # Your code where you can use urlopen
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    response = opener.open(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup

class TokenTransaction:
  def __init__(self, token_name,tx_hash,timestamp,from_account,to_account,quantity):
    self.token_name = token_name
    self.tx_hash = tx_hash
    self.timestamp = timestamp
    self.from_account = from_account
    self.to_account = to_account
    self.quantity = quantity

def get_transcripts_at_p(token_name,p):
  base_url = 'https://etherscan.io/token/generic-tokentxns2?contractAddress=0xe41d2489571d322189246dafa5ebde1f4699f498&p={}'.format(p)
  soup = get_html_by_url(base_url)
  arrs = soup.findAll('tr')
  transactions = []
  for x in range(1,len(arrs)):
    arr = arrs[x]
    tds = arr.findAll('td')
    txhash = ""
    timestamp = ""
    from_account = ""
    to_account = ""
    quantity = ""
    for y in range(0,len(tds)):
       td = tds[y]
       if y == 0:
         #txhash
         txhash = td.text
       elif y == 1:
         #timestamp
         timestamp = td.find("span")["title"]
         timestamp = parser.parse(timestamp)
       elif y == 2:
         #from
         from_account = td.find("span").find('a').text
       elif y == 4:
         # to
         to_account = td.find("span").find("a").text
       elif y == 5:
         # quantity
         quantity = td.text
    token_transaction = TokenTransaction(token_name,txhash,timestamp,from_account,to_account,quantity)
    transactions.append(token_transaction)
  return transactions

transactions = get_transcripts_at_p("0x",1)
