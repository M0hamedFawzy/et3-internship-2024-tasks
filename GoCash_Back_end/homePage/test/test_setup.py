from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from users.models import User
from SubscriptionPlan.models import SubscriptionPlan
from rest_framework.authtoken.models import Token
from faker import Faker


def fake_phone_number(fake: Faker) -> str:
    return f'+02 {fake.msisdn()[3:]}'


class TestSetup(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.sign_in_url = reverse('sign_in')
        self.logout_url = reverse('logout')
        self.fake = Faker()

        # self.fake_phone_number = fake_phone_number(self.fake)

        self.user_data = {
            "username": "TestUser1",
            "phone_number": "1111",
        }

        # Create a user for sign_in tests
        default_plan = SubscriptionPlan.objects.get(id=1)
        self.user = User.objects.create_user(
            username=self.user_data['username'],
            phone_number=self.user_data['phone_number'],
            password=None,
            subscription_plan=default_plan
        )
        self.token = Token.objects.create(user=self.user)

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
