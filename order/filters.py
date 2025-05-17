import django_filters
from core.models import Order, OrderItem

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = ['status', 'created_at']  # Câmpuri care EXISTĂ în model

class OrderItemFilter(django_filters.FilterSet):
    class Meta:
        model = OrderItem
        fields = ['order', 'menu_item']  # Câmpuri care EXISTĂ în model
