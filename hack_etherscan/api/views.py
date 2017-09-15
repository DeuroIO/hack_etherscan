# api/views.py

from rest_framework import generics
from .serializers import TokenTransactionSerializer
from polls.models import TokenTransaction

class CreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = TokenTransaction.objects.all()
    serializer_class = TokenTransactionSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()