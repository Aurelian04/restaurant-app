from rest_framework import serializers
from core.models import MenuItem
from core.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['menu_item', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'items', 'status', 'created_at', 'total_price']
        read_only_fields = ['id', 'status', 'created_at', 'total_price']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user

        order = Order.objects.create(user=user)

        total_price = 0
        for item_data in items_data:
            menu_item = MenuItem.objects.get(id=item_data['menu_item'].id)
            quantity = item_data['quantity']
            price = menu_item.price * quantity

            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=quantity,
                price=menu_item.price
            )

            total_price += price

        order.total_price = total_price
        order.save()

        return order
