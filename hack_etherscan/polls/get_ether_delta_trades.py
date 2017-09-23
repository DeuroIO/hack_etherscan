import requests

ether_delta_orders_api = "https://api.etherdelta.com/trades"
def get_ether_delta_trade_for(contract_address,page):
  r = requests.get("{}/{}/{}".format(ether_delta_orders_api,contract_address,page))
  r_json = r.json()
  return r_json
