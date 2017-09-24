# api/urls.py

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import RetriveTopTokenHolderView,RetriveTopTokenTransactionView,update_account,add_token,get_all_tokens,get_etherdelta_input_for_zerox,get_kyber_stat_on_etherdelta

urlpatterns = {
    url(r'^topTokenHolders/(?P<time>\d+)/(?P<token>[\w\-]+)/$', RetriveTopTokenHolderView.as_view(), name="top_holder"),
    url(r'^topTokenTransactions/(?P<time>\d+)/(?P<token>[\w\-]+)/$', RetriveTopTokenTransactionView.as_view(), name="top_transaction"),
    url(r'^update_account/(?P<account>[\w\-]+)/$', update_account, name="update_account"),
    url(r'^add_token/(?P<token>[\w\-]+)/(?P<token_name>[\w\-]+)$', add_token, name="add_token"),
    url(r'^get_all_tokens/$', get_all_tokens, name="get_all_tokens"),
    #etherdelta
    url(r'^get_etherdelta_input_for_zerox$', get_etherdelta_input_for_zerox, name="get_etherdelta_input_for_zerox"),
    #check web3 kyber etherdelta stat
    url(r'^get_kyber_stat_on_etherdelta/(?P<timestamp>\d+)$', get_kyber_stat_on_etherdelta, name="get_kyber_stat_on_etherdelta")
}

urlpatterns = format_suffix_patterns(urlpatterns)
