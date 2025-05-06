"""
Test for models.
"""


from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email="user@example.com", password="testpass123"):
    """Create and return a new user."""
    return get_user_model().objects.create(email, password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_succesful(self):
        """Test creating a user with an email succesful."""
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        