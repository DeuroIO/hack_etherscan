from .html_helper import get_html_by_url
from .models import Token,TokenTransaction, Account
from dateutil import parser
from celery.decorators import periodic_task,task
from celery.task.schedules import crontab
from .crawl import get_transcripts_at_p,get_html_by_url

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

        transaction = TokenTransaction(token_name=m_token, tx_hash=txhash, timestamp=timestamp,
                                       from_account=m_from_account_o, to_account=m_to_account_o,
                                       quantity=float(quantity))

        try:
            transaction.save()
        except:
            pass
    
        

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
