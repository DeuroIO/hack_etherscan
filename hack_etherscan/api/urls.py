# api/urls.py

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import RetriveTopTokenHolderView,RetriveTopTokenTransactionView,update_account,add_token,get_all_tokens

urlpatterns = {
    url(r'^topTokenHolders/(?P<time>\d+)/(?P<token>[\w\-]+)/$', RetriveTopTokenHolderView.as_view(), name="top_holder"),
    url(r'^topTokenTransactions/(?P<time>\d+)/(?P<token>[\w\-]+)/$', RetriveTopTokenTransactionView.as_view(), name="top_transaction"),
    url(r'^update_account/(?P<account>[\w\-]+)/$', update_account, name="update_account"),
    url(r'^add_token/(?P<token>[\w\-]+)/(?P<token_name>[\w\-]+)$', add_token, name="add_token"),
    url(r'^get_all_tokens/$', get_all_tokens, name="get_all_tokens")
}

urlpatterns = format_suffix_patterns(urlpatterns)
