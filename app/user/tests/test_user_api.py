from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status  # makes tests easier to read


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):  # think of Public as un-authenticated
    """Test the users API (public)"""
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test crating user with valid payload is successful"""
        payload = {
            'email': 'test@mail.com',
            'password': 'test123',
            'name': 'Test User'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)  # avoid passwd returning

    def test_user_exists(self):
        """Test creating an existing user fails"""
        payload = {
            'email': 'test@mail.com',
            'password': 'test123',
            'name': 'Test User',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password is > 5 characters"""
        payload = {
            'email': 'test@mail.com',
            'password': '123',
            'name': 'Test User'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)
