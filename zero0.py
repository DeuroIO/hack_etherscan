import csv
from dateutil import parser
import datetime
import locale
locale.setlocale(locale.LC_ALL, 'en_US')
import collections

def parse_time_to_hour(timestamp):
    old_date = parser.parse(timestamp)
    new_date = old_date.replace(hour=0,minute=0, second=0)
    # new_date = old_date.replace(second=0)
    return new_date

class TokenTransaction(object):
    def __str__(self):
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S") + ": from " + self.from_account + " to " + self.to_account + " " + str(self.quantity)
    def __init__(self,token_name,tx_hash,timestamp,from_account,to_account,quantity):
        self.token_name = token_name
        self.tx_hash = tx_hash
        self.timestamp = parse_time_to_hour(timestamp)
        self.from_account = from_account
        self.to_account = to_account
        self.quantity = float(quantity.replace(",",""))

top_limit = 50

def read_csv():
    csvfile = open('0x.csv')
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

    all_the_records = dict()
    row_number = 0
    for row in spamreader:
        row_number += 1
        if row_number == 1:
            #header
            continue
        else:
            token_name,tx_hash,timestamp,from_account,to_account,quantity = row
            t = TokenTransaction(token_name,tx_hash,timestamp,from_account,to_account,quantity)
            if t.timestamp in all_the_records:
                all_the_records[t.timestamp].append(t)
            else:
                all_the_records[t.timestamp] = [t]

    #compute top_timestamp_token_holder_dict

    #sort the dictionary by key: timestamp
    od = collections.OrderedDict(sorted(all_the_records.items()))
    current_account_balance_dict = dict()
    top_timestamp_token_holder_dict = dict()

    for timestamp, arr in od.items():
        for transaction in arr:
            targeted_account = transaction.to_account
            transaction_amount = transaction.quantity
            if transaction.to_account not in current_account_balance_dict:
                current_account_balance_dict[targeted_account] = transaction_amount
            else:
                current_account_balance_dict[targeted_account] += transaction_amount

        top_token_holder_accounts = sorted(current_account_balance_dict, key=lambda k: current_account_balance_dict[k],reverse=True)[:top_limit]

        top_holder_balance_arr = []
        for account in top_token_holder_accounts:
            top_holder_balance_arr.append([account,current_account_balance_dict[account]])

        top_timestamp_token_holder_dict[timestamp] = top_holder_balance_arr

    return all_the_records,top_timestamp_token_holder_dict

def generate_table(all_the_records,timestamp):
    test_date = parse_time_to_hour(timestamp)
    print(test_date)
    filtered_records = sorted(all_the_records[test_date],key=lambda x: x.quantity, reverse=True)[:top_limit]

    rank = 1
    for record in filtered_records:
        print("{}\t{}\t{}\t{}%".format(rank,record.to_account,locale.format("%d", int(record.quantity), grouping=True),record.quantity / 5000000))
        rank += 1

def generate_token_holder_table(top_timestamp_token_holder_dict,timestamp):
    test_date = parse_time_to_hour(timestamp)
    print(test_date)

    rank = 1
    top_token_holder_accounts = top_timestamp_token_holder_dict[test_date]
    for (account,balance) in top_token_holder_accounts:
        print("{}\t{}\t{}".format(rank,account,locale.format("%d", int(balance), grouping=True)))
        rank += 1

#testing

# all_the_records,top_timestamp_token_holder_dict = read_csv()
# generate_token_holder_table(top_timestamp_token_holder_dict,"2017-06-09 18:05:00")
