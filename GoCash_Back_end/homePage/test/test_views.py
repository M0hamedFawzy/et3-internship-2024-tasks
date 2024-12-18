from .test_setup import TestSetup
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User
from SubscriptionPlan.models import SubscriptionPlan
from rest_framework.authtoken.models import Token
from rest_framework import status


class TestViews(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.sign_in_url = reverse('sign_in')
        self.logout_url = reverse('logout')

        # Create a default subscription plan in the test database
        self.default_plan = SubscriptionPlan.objects.create(
            id=1, name='Standard', price=10.0  # Ensure the fields match your model
        )

        self.user_data = {
            "username": "TestUser1",
            "phone_number": "1111"
        }

        self.user = User.objects.create_user(
            username="StaticUser",
            phone_number="0000",
            password="testpassword",
            subscription_plan=self.default_plan
        )
        self.token = Token.objects.create(user=self.user)

    def test_register_user_with_valid_data(self):
        # Test user registration with valid data (happy scenario)
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertIn('token', response.data['user'])
        self.assertEqual(response.data['user']['username'], self.user_data['username'])
        self.assertEqual(response.data['user']['phone_number'], self.user_data['phone_number'])

    def test_register_user_with_no_data(self):
        # Test user registration with no data (sad scenario)
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_existing_user(self):
        # Test user that already exists (sad scenario)
        user_data = {
            "username": "StaticUser",
            "phone_number": "0000"
        }
        response = self.client.post(self.register_url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_non_numerical_phone_number(self):
        # Test register with nonnumerical phone number (sad scenario)
        user_data = {
            "username": "StaticUser",
            "phone_number": "ABCD"
        }
        response = self.client.post(self.register_url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_in_nonexistent_user(self):
        user_data = {
            "username": "TestUser2",
            "phone_number": "2222"
        }
        response = self.client.post(self.sign_in_url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)



