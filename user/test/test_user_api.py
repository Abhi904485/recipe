"""User Api Tests"""

from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER = reverse('user:create')
CREATE_TOKEN = reverse('user:token')
ME_URL = reverse('user:me')


def create_new_user(params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public feature of Api tests"""

    def setUp(self):
        """Setting Up Public User Api Test"""
        self.client = APIClient()
        self.payload = {
            "email": "Abhishek@DEEPFENCE.io",
            'password': "Novell@123",
            'name': "Abhishek"
        }
        self.normalize_email = "Abhishek@deepfence.io"

    def test_create_user_success(self):
        """Test creating a user is successful"""
        res = self.client.post(path=CREATE_USER, data=self.payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=self.normalize_email)
        self.assertTrue(user.check_password(self.payload["password"]))
        self.assertEqual(user.email, self.normalize_email)

    def test_create_user_failed(self):
        """Test creating a user is Failed"""

        payload = {
            "email": "Abhishek@DEEPFENCE.io",
            'password': "Novell@123",
        }
        res = self.client.post(path=CREATE_USER, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_with_email_exists_error(self):
        """Test User with email already Exists"""
        create_new_user(self.payload)
        res = self.client.post(path=CREATE_USER, data=self.payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_password_too_short_error(self):
        """Test user with password to short"""
        payload = {
            "email": "Abhishek@DEEPFENCE.io",
            'password': "abc",
            'name': "Abhishek"
        }
        res = self.client.post(path=CREATE_USER, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload["email"]).exists()
        self.assertFalse(user_exists)

    def test_create_token_user(self):
        """Create Token For New user"""
        create_new_user(self.payload)
        payload = {
            "username": "Abhishek@deepfence.io",
            'password': "Novell@123",
        }
        res = self.client.post(path=CREATE_TOKEN, data=payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_for_user_empty_password(self):
        """Test Create Token For User having Empty Password"""
        create_new_user(self.payload)
        payload = {
            "username": "Abhishek@deepfence.io",
            'password': "",
        }
        res = self.client.post(path=CREATE_TOKEN, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_for_user_wrong_password(self):
        """Test Create Token For User having Empty Password"""
        create_new_user(self.payload)
        payload = {
            "username": "Abhishek@deepfence.io",
            'password': "Novell@124",
        }
        res = self.client.post(path=CREATE_TOKEN, data=payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_retrieve_user_unauthorized(self):
        """Test Case to Throw Unauthorized for not Logged-In user"""
        create_new_user(self.payload)
        res = self.client.get(path=ME_URL, data={})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test Api That Require Authentication"""

    def setUp(self):
        self.client = APIClient()
        self.payload = {
            "email": "Abhishek@deepfence.io",
            'password': "Novell@123",
            'name': "Abhishek"
        }
        self.user = create_new_user(self.payload)
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test For User Profile Retrieval Success"""
        res = self.client.get(path=ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {"name": self.user.name,
                                    "email": self.user.email})

    def test_post_me_not_allowed(self):
        """Test For User Post method is not Allowed"""
        res = self.client.post(path=ME_URL, data=self.payload)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_profile_success(self):
        """Test For User Profile Update Success"""
        payload = {
            "email": "Abhishek@gmail.com",
            'password': "Novell@1234",
            'name': "Abhishek Updated"
        }
        res = self.client.put(path=ME_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {"name": payload["name"],
                                    "email": self.payload["email"]})
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertFalse(self.user.check_password(self.payload["password"]))

    def test_patch_password_success(self):
        """Test Patch User Password"""
        payload = {
            'password': "Novell@1235",
        }
        res = self.client.patch(path=ME_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password(payload["password"]))

    def test_patch_username_success(self):
        """Test Patch Username Success"""
        payload = {
            'name': "James Bond",
        }
        res = self.client.patch(path=ME_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload["name"])

    def test_patch_email_no_effect(self):
        """Test Patch Email No Effect"""
        payload = {
            'email': "Abhishek@deepfence.go",
        }
        res = self.client.patch(path=ME_URL, data=payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, self.payload["email"])
        self.assertNotEqual(self.user.email, payload["email"])
