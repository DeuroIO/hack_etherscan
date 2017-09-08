import csv
from dateutil import parser
import datetime
import locale
locale.setlocale(locale.LC_ALL, 'en_US')
def parse_time_to_hour(timestamp):
    old_date = parser.parse(timestamp)
    new_date = old_date.replace(hour=0,minute=0, second=0)
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
    return all_the_records

def generate_table(all_the_records,timestamp):
    test_date = parse_time_to_hour(timestamp)
    print(test_date)
    filtered_records = sorted(all_the_records[test_date],key=lambda x: x.quantity, reverse=True)[:50]

    rank = 1
    for record in filtered_records:
        print("{}\t{}\t{}\t{}%".format(rank,record.to_account,locale.format("%d", int(record.quantity), grouping=True),record.quantity / 5000000))
        rank += 1
