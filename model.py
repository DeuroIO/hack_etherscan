class TokenTransaction:
  def __init__(self, token_name,tx_hash,timestamp,from_account,to_account,quantity):
    self.token_name = token_name
    self.tx_hash = tx_hash
    self.timestamp = timestamp
    self.from_account = from_account
    self.to_account = to_account
    self.quantity = quantity
