"""
Testt for Menu.
"""

from django.test import TestCase
from core.models import MenuItem


class MenuModelTests(TestCase):
    """Test for menu item model."""

    def test_create_menu_item_successful(self):
        """Test creating a menu item is successful and saved in DB correctly."""
        item = MenuItem.objects.create(
            name="Pizza Pollo",
            description="Classic pizza with tomato and cheese.",
            price=25.00,
            category="main",
            available=True
        )

        self.assertEqual(str(item), item.name)
        self.assertEqual(item.price, 25.00)
        self.assertTrue(item.available)