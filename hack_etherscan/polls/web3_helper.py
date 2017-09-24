from web3 import Web3, HTTPProvider, IPCProvider
web3 = Web3(HTTPProvider('http://localhost:8545'))
from datetime import datetime
#Get deposit  & withdraw transactions for a token_address
def getTransactionsByAccount(myaccount, token_address,block_number):
    matched_transactions = []
    block = web3.eth.getBlock(block_number, True)
    if block is not None and block.transactions is not None:
        transactions = block["transactions"]
        for transaction in transactions:
            if transaction["from"] == myaccount or transaction["to"] == myaccount:
                if token_address in transaction["input"]:
                    matched_transactions.append(transaction)
    raw_timestamp = web3.eth.getBlock(block_number).timestamp
    timestamp = datetime.utcfromtimestamp(raw_timestamp)
    return matched_transactions,timestamp
