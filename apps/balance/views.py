from rest_framework.viewsets import ModelViewSet
from .models import Transaction, Balance
from .serializers import BalanceSerializer, TransactionSerializer


class BalanceViewSet(ModelViewSet):
    queryset = Balance.objects.all()
    serializer_class = BalanceSerializer


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


