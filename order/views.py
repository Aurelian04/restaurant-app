from rest_framework import generics, permissions
from core.models import Order
from order.serializers import OrderSerializer

class CreateOrderView(generics.CreateAPIView):
    """API view pentru plasarea unei comenzi."""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
