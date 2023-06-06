"""Test For Django Admin Modifications"""

from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase, Client


class AdminSiteTests(TestCase):
    """Tests For Django Admin"""

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="Admin@deepfence.io", password="Admin@123")
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="Abhishek@deepfence.io", password="Abhishek@123",
            name="Test User")

    def test_user_list(self):
        """Test User List Page"""
        url = reverse("admin:core_user_changelist")
        res = self.client.get(path=url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_edit_page(self):
        """Test User Edit Page"""
        url = reverse("admin:core_user_change",
                      kwargs={'object_id': self.user.pk})
        res = self.client.get(path=url)
        self.assertEqual(res.status_code, 200)
