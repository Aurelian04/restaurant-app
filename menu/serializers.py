from rest_framework import serializers
from core.models import MenuItem

class MenuItemSerializer(serializers.ModelSerializer):
    """Serializer for the menu item."""

    class Meta:
        model = MenuItem
        fields = [
            'id',
            'name',
            'description',
            'price',
            'category',
            'available',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_price(self, value):
        """Price is >= 0."""
        if value <= 0:
             raise serializers.ValidationError("Prețul trebuie să fie mai mare decât 0.")
        return value
    
    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Numele nu poate fi gol sau doar spații.")
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Numele trebuie să aibă cel puțin 3 caractere.")
        return value

    def validate(self, attrs):
        """Elimină câmpul 'available' pentru userii care nu sunt staff."""
        request = self.context.get('request')
        if request and not request.user.is_staff:
            attrs.pop('available', None)  # Ignoră orice încercare de a seta available
        return attrs