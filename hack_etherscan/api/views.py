# api/views.py

from rest_framework import generics
from .serializers import TopTokenHolderSerializer,TopTokenTransactionsSerializer
from polls.models import TopTokenHolder,TopTokenTransaction,Account
from dateutil import parser
from django.http import JsonResponse,HttpResponse

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
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_account(request,account):
    memo = request.POST.get("memo",None)
    if memo is None:
        response = JsonResponse({'status':'false'}, status=400)
        return response
    account_obj = Account.objects.get(account_address=account)
    account_obj.gussed_name = memo
    account_obj.save()
    return JsonResponse({"status":"okay"})
