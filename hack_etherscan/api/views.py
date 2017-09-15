# api/views.py

from rest_framework import generics
from .serializers import TopTokenHolderSerializer,TopTokenTransactionsSerializer
from polls.models import TopTokenHolder,TopTokenTransaction
from dateutil import parser

class RetriveTopTokenHolderView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = TopTokenHolder.objects.all()
    serializer_class = TopTokenHolderSerializer
    lookup_url_kwarg = "time"

    def get_queryset(self):
        timestamp_s = self.kwargs.get(self.lookup_url_kwarg)
        timestamp = parser.parse(timestamp_s)
        holders = TopTokenHolder.objects.filter(timestsamp=timestamp)
        return holders

class RetriveTopTokenTransactionView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = TopTokenTransaction.objects.all()
    serializer_class = TopTokenTransactionsSerializer
    lookup_url_kwarg = "time"

    def get_queryset(self):
        timestamp_s = self.kwargs.get(self.lookup_url_kwarg)
        timestamp = parser.parse(timestamp_s)
        transactions = TopTokenTransaction.objects.filter(timestsamp=timestamp)
        return transactions