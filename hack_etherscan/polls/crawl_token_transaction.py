from dateutil import parser
# from models import TokenTransaction
import multiprocessing
#
# from html_helper import get_html_by_url
# from db_helper import save_array_of_objs_to_db

def get_transactions_at_p(token_name,p):
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


num_worker_threads = 34
pool = multiprocessing.Pool(processes=num_worker_threads)

for x in range(1,2458):
  pool.apply_async(get_transactions_at_p, args=("0x",x), callback=save_array_of_objs_to_db)

pool.close()
pool.join()
