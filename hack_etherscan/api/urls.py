# api/urls.py

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import RetriveTopTokenHolderView,RetriveTopTokenTransactionView

urlpatterns = {
    url(r'^topTokenHolders/(?P<time>\d+)/$', RetriveTopTokenHolderView.as_view(), name="top_holder"),
    url(r'^topTokenTransactions/(?P<time>\d+)/$', RetriveTopTokenTransactionView.as_view(), name="top_transaction"),
}

urlpatterns = format_suffix_patterns(urlpatterns)