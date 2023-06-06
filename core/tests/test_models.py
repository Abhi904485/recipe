"""Tests For Models"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Recipe


class ModelTest(TestCase):
    """Test Models."""

    def test_create_user_email_success(self):
        """Test Creating A user With Email Success"""
        email = "Abhishek@gmail.com"
        password = "Novell@123"
        user = get_user_model().objects.create_user(email=email,
                                                    password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test Email is Normalized for new users"""
        sample_emails = [['Abhishek1@GMAIL.com', 'Abhishek1@gmail.com'],
                         ['Abhishek2@Gmail.COM', 'Abhishek2@gmail.com']]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email=email,
                                                        password="sample@123")
            self.assertEqual(user.email, expected)

    def test_create_super_user(self):
        """Test Create Super User"""
        email = "Abhishek@gmail.com"
        password = "Novell@123"
        user = get_user_model().objects.create_superuser(email=email,
                                                         password=password)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_recipe_success(self):
        """Test Create Recipe Success"""
        user_payload = {
            "email": "Abhishek@deepfence.io",
            "password": "Novell@123"
        }
        user = get_user_model().objects.create_user(**user_payload)
        recipe_payload = {
            "title": "Recipe 1",
            "price": Decimal("23.45"),
            "description": "Recipe 1 Description",
            "time_minutes": 5,
            "user": user

        }
        recipe = Recipe.objects.create(**recipe_payload)
        self.assertEqual(str(recipe), recipe_payload["title"])
