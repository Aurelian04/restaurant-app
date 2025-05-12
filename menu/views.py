from rest_framework import generics, authentication, permissions
from core.models import MenuItem
from menu.serializers import MenuItemSerializer
from menu.permissions import IsStaffUser


class BaseMenuItemView:
    """Common settings for menu item views."""
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsStaffUser]

class MenuView(BaseMenuItemView, generics.CreateAPIView):
    """Create a menu item (staff only)."""
    pass

class UpdateMenuItemView(BaseMenuItemView, generics.UpdateAPIView):
    """Update a menu item (staff only)."""
    pass

class PublicMenuView(generics.ListAPIView):
    """Public view to list all menu list for everyone."""
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    authentication_classes = []
    permission_classes = []
