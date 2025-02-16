from venv import logger

from rest_framework import viewsets, permissions
from .models import Order
from .serializers import OrderSerializer
from .models import Transaction
from .serializers import TransactionSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        logger.info(f"1!!!!!!!!!!!!!!!!")

class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
