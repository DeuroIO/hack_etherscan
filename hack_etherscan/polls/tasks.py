from .html_helper import get_html_by_url
from .models import Token,TokenTransaction, Account,TopTokenTransaction,TopTokenHolder
from dateutil import parser
from celery.decorators import periodic_task,task
from .crawl import get_transcripts_at_p,get_html_by_url
import datetime
from collections import OrderedDict

@task(name="get_token_tx_from_a_page")
def get_token_tx_from_a_page(coin_name,contract_address,page_num):
    transactions = get_transcripts_at_p(coin_name, contract_address,page_num)
    for transaction in transactions:
        (token_name,txhash,timestamp,from_account,to_account,quantity) = transaction
        from_account_o = Account(gussed_name="", account_address=from_account)
        to_account_o = Account(gussed_name="", account_address=to_account)

        try:
            from_account_o.save()
        except:
            pass

        try:
            to_account_o.save()
        except:
            pass

        m_token = Token.objects.get(contract_address=contract_address)
        m_from_account_o = Account.objects.get(account_address=from_account)
        m_to_account_o = Account.objects.get(account_address=to_account)
        try:
            float_quantity = float(quantity)
        except:
            continue
        transaction = TokenTransaction(token_name=m_token, tx_hash=txhash, timestamp=timestamp,
                                       from_account=m_from_account_o, to_account=m_to_account_o,
                                       quantity=float_quantity)

        try:
            transaction.save()
        except:
            pass
@task(name="calculate_today_top_stat")
def calculate_today_top_stat(contract_address):

    today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    today = datetime.datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)

    m_token = Token.objects.get(contract_address=contract_address)
    transactions = TokenTransaction.objects.filter(token_name=m_token,timestamp__range=(today_min,today_max)).order_by("-quantity")

    top_limit = 20
    
    before_top_tx_time = datetime.datetime.now()
    # top tx
    top_txs = TopTokenTransaction.objects.filter(timestsamp=today,token_name=m_token)
    if top_txs:
        top_txs.delete()
    print("delete old top_txs :{}".format(datetime.datetime.now()-before_top_tx_time))

    before_tx_save = datetime.datetime.now()
    rank = 1
    for x in range(0,top_limit):
        tx = TopTokenTransaction(token_name=m_token,timestsamp=today,transaction=transactions[x],rank=rank)
        tx.save()
        rank += 1
    print("save tx :{}".format(datetime.datetime.now()-before_tx_save))

    # top token holder
    current_account_balance_dict = dict()
    before_build_top_token_holder_dict = datetime.datetime.now()
    for transaction in transactions:
        transaction_amount = transaction.quantity
        targeted_account = transaction.to_account

        if targeted_account not in current_account_balance_dict:
            current_account_balance_dict[targeted_account] = transaction_amount
        else:
            current_account_balance_dict[targeted_account] += transaction_amount
    sorted_current_account = sorted(current_account_balance_dict.items(), key=lambda x: x[1],reverse=True)
    sorted_current_account = sorted_current_account[:top_limit]
    print("build top_token_holder_dict:{}".format(datetime.datetime.now()-before_build_top_token_holder_dict))

    holders = TopTokenHolder.objects.filter(timestsamp=today,token_name=m_token)
    if holders:
        holders.delete()
    
    rank = 1
    for account,amount in sorted_current_account:
        holder = TopTokenHolder(token_name=m_token,timestsamp=today,account=account,top_amount=amount,rank=rank)
        holder.save()
        rank += 1

#get all tokens from https://etherscan.io/tokentxns
@task(name="get_tokens_from_view_a_tokentxns_page")
def get_tokens_from_view_a_tokentxns_page(base_url):

    soup = get_html_by_url(base_url)
    tbody = soup.find('tbody')
    trs = tbody.find_all("tr")
    for x in range(1, len(trs)):
        tr = trs[x]
        tds = tr.findAll('td')
        txhash = ""
        timestamp = ""

        from_account = ""
        from_account_name = ""

        to_account = ""
        to_account_name = ""

        quantity = ""
        token_name = ""
        token_contract_address = ""
        for y in range(0, len(tds)):
            td = tds[y]
            if y == 0:
                # txhash
                txhash = td.text
            elif y == 1:
                # timestamp
                timestamp = td.find("span")["title"]
                timestamp = parser.parse(timestamp)
            elif y == 2:
                # from
                from_account = td.find("span").find('a')["href"][9:-10]
                from_account_name = td.find("span").find("a").text
                if from_account == from_account_name:
                    from_account_name = ""
            elif y == 4:
                # to
                to_account = td.find("span").find("a")["href"][9:-10]
                to_account_name = td.find("span").find("a").text
                if to_account == to_account_name:
                    to_account_name = ""
            elif y == 5:
                # quantity
                quantity = td.text.replace(",", "")
            elif y == 6:
                tmp_a = td.find("a")
                token_name = tmp_a.text
                token_contract_address = tmp_a["href"][7:-3]
        token = Token(coin_name=token_name, contract_address=token_contract_address)
        from_account_o = Account(gussed_name=from_account_name, account_address=from_account)
        to_account_o = Account(gussed_name=to_account_name, account_address=to_account)

        try:
            token.save()
        except:
            pass

        try:
            from_account_o.save()
        except:
            pass

        try:
            to_account_o.save()
        except:
            pass

        m_token = Token.objects.get(contract_address=token_contract_address)
        print(from_account)
        m_from_account_o = Account.objects.get(account_address=from_account)
        print(to_account)
        m_to_account_o = Account.objects.get(account_address=to_account)

        transaction = TokenTransaction(token_name=m_token, tx_hash=txhash, timestamp=timestamp,
                                       from_account=m_from_account_o, to_account=m_to_account_o,
                                       quantity=float(quantity))

        try:
            transaction.save()
        except:
            pass
