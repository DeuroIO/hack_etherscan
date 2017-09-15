from bs4 import BeautifulSoup
from dateutil import parser
from urllib.request import build_opener


def get_html_by_url(url):
    opener = build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    response = opener.open(url)
    html = response.read()
    soup = BeautifulSoup(html)
    return soup

def get_transcripts_at_p(token_name,contract_address,p):
  base_url = 'https://etherscan.io/token/generic-tokentxns2?contractAddress={}&p={}'.format(contract_address,p)
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
    transactions.append([token_name,txhash,timestamp,from_account,to_account,quantity])
  return transactions
