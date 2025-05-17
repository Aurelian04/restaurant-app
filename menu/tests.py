"""
Testt for Menu.
"""

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from core.models import MenuItem, User, Order, OrderItem
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from decimal import Decimal

CREATE_MENU_URL = reverse('menu:create-item')
GET_MENU = reverse('menu:public-menu')



def create_user(**params):
    return get_user_model().objects.create_user(**params)

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

    def test_menu_item_without_name_raises_error(self):
        """Test model validation raises error when name is missing."""
        item = MenuItem(price=25.0)
        with self.assertRaises(ValidationError):
            item.full_clean() 

class PrivateMenuApiTests(TestCase):
    """Tests for staff API related to menu items."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email="test@example.com", 
            password="testpass123", 
            is_staff=True
        )
        self.client.force_authenticate(user=self.user)

    def test_create_menu_item(self):
        """Test that staff user can create a menu item successfully."""
        payload = {
            'name': 'Pizza Margherita',
            'price': '30.0',
            'description': 'Classic Italian pizza with mozzarella and basil.',
            'category': 'main',
        }

        res = self.client.post(CREATE_MENU_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        item_exists = MenuItem.objects.filter(
            name=payload['name'],
            price=payload['price'],
            category=payload['category']
        ).exists()

        self.assertTrue(item_exists)

    def test_create_item_without_name(self):
        """Test create an item without a name."""
        payload = {
            'name': '',
            'price': '30.0',
            'description': 'Classic Italian pizza with mozzarella and basil.',
            'category': 'main',
        }
        res = self.client.post(CREATE_MENU_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_menu_item_unauthorized(self):
        """Test that authentication is required to create manu item. """
        client = APIClient()
        payload = {'name': 'Pizza', 'price': '25.00', 'category': 'Main'}
        res = client.post(CREATE_MENU_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_menu_item(self):
        """Test that a staff user can update a menu item."""
        item = MenuItem.objects.create(
            name="Pizza Margherita",
            price="30.00",
            description="Classic pizza",
            category="pizza"
        )

        payload = {"price": "35.00", "description": "Updated description"}
        url = reverse("menu:update-item", args=[item.id])
        res = self.client.patch(url, payload)

        item.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(item.price, Decimal(payload["price"]))
        self.assertEqual(item.description, payload["description"])

class PublicMenuApiTests(TestCase):
    """Testes for public api menu."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email="test@example.com", 
            password="testpass123",
        )

    def test_get_menu_works(self):
        """Test get the menu list works."""
        MenuItem.objects.create(name="Pizza", price=25.5, category="main")
        MenuItem.objects.create(name="Tocinei", price=15.0, category="dessert")

        res = self.client.get(GET_MENU)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

        item_names = [item["name"] for item in res.data]
        self.assertIn("Pizza", item_names)
        self.assertIn("Tocinei", item_names)
    
    def test_get_menu_works(self):
        url = reverse('menu:public-menu')
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)


class OrderApiTests(TestCase):
    """Tests for the Order API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='test@example.com', password='testpass123')
        self.client.force_authenticate(user=self.user)

        # Creăm două produse în meniu
        self.item1 = MenuItem.objects.create(
            name='Pizza',
            description='Delicious pizza',
            price=Decimal('25.00'),
            category='main',
            available=True
        )
        self.item2 = MenuItem.objects.create(
            name='Cola',
            description='Cold drink',
            price=Decimal('5.00'),
            category='drink',
            available=True
        )

        # Corect: reverse este apelat în setUp, după ce URL-urile au fost încărcate
        self.create_order_url = reverse('order:order-list')

    def test_create_order_successful(self):
        """Test that a user can successfully place an order."""
        payload = {
            "items": [
                {"menu_item": self.item1.id, "quantity": 2},  # 2 x Pizza = 50.00
                {"menu_item": self.item2.id, "quantity": 3}   # 3 x Cola = 15.00
            ]
        }

        res = self.client.post(self.create_order_url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Verificăm că s-a creat comanda și produsele din comandă
        order = Order.objects.get(id=res.data['id'])
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.total_price, Decimal('65.00'))  # 50 + 15

        order_items = order.items.all()
        self.assertEqual(order_items.count(), 2)

        # Verificăm că produsele și cantitățile sunt corecte
        item_quantities = {item.menu_item.name: item.quantity for item in order_items}
        self.assertEqual(item_quantities['Pizza'], 2)
        self.assertEqual(item_quantities['Cola'], 3)

    def test_update_order_status_success(self):
        """Test is user can refresh order status."""
        order = Order.objects.create(user=self.user, total_price=100.0)
        url = reverse('order:order-detail', args=[order.id])

        res = self.client.patch(url, {"status": "preparing"}, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.status, "preparing")

    def test_non_staff_cannot_mark_order_delivered(self):
        "Test non-staff user cannot set order status."
        order = Order.objects.create(user=self.user, total_price=100.0)
        url = reverse('order:order-detail', args=[order.id])

        res = self.client.patch(url, {"status": "delivered"}, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)